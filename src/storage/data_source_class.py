from datetime import datetime
from uuid import uuid4

from pydantic import UUID4

from authentication.access_control import assert_user_has_access
from authentication.models import AccessControlList, AccessLevel, User
from common.exceptions import (
    BadRequestException,
    MissingPrivilegeException,
    NotFoundException,
)
from common.utils.logging import logger
from common.utils.string_helpers import url_safe_name
from domain_classes.document_look_up import DocumentLookUp
from domain_classes.repository import Repository
from domain_classes.storage_recipe import StorageAttribute
from enums import StorageDataTypes
from services.database import acl_lookup_db, document_cache

DOCUMENT_CACHE_TTL = 60 * 60 * 24  # 24 hours


class DataSource:
    """
    A DataSource instance is an abstraction layer over several repositories(databases/storage backends).
    Access Control is done in the DataSource based on the Access Control Lists defined in the internal lookup tables.
    """

    def __init__(
        self,
        name: str,
        user: User,
        acl: AccessControlList = AccessControlList.default(),
        repositories=None,
        acl_lookup_db=acl_lookup_db,
        document_cache=document_cache,
    ):
        self.name = name
        self.user = user
        # This Access Control List (ACL) is used when there is no parent to inherit ACL from. Controls who can create root-packages.
        self.acl = acl
        self.repositories: dict[str, Repository] = repositories
        self.acl_lookup_db = acl_lookup_db
        self.document_cache = document_cache

    @classmethod
    def from_dict(cls, a_dict, user: User, get_blueprint):
        return cls(
            a_dict["name"],
            user,
            AccessControlList(**a_dict.get("acl", AccessControlList.default().to_dict())),
            {
                key: Repository(name=key, get_blueprint=get_blueprint, **value)
                for key, value in a_dict["repositories"].items()
            },
        )

    def _get_repo_from_storage_attribute(self, storage_attribute: StorageAttribute = None, strict=False) -> Repository:
        # Not too smart yet...
        # Returns the first repo with a matching "dataType" value, or the first Repo if no match
        if storage_attribute:
            for r in self.repositories.values():
                if storage_attribute.storage_affinity in r.data_types:
                    return r
        if strict:
            raise ValueError(f"No repository for '{storage_attribute.storage_affinity}' data configured")
        return self.get_default_repository()

    # TODO: Read default attribute from DataSource spec
    def get_default_repository(self) -> Repository:
        # Now just returns the first repo in the ordered_dict
        return next(iter(self.repositories.values()))

    def _lookup(self, document_id) -> DocumentLookUp:
        if res := self.acl_lookup_db.get(f"{self.name}:{document_id}"):
            return DocumentLookUp(**res)

        raise NotFoundException(
            message=f"Document with id '{document_id}' was not found in the '{self.name}' data-source"
        )

    def get_storage_affinity(self, document_id) -> StorageDataTypes:
        lookup = self._lookup(document_id)
        return StorageDataTypes(lookup.storage_affinity)

    def _update_lookup(self, lookup: DocumentLookUp):
        return self.acl_lookup_db.set(f"{self.name}:{lookup.database_id}", lookup.dict())

    def update_access_control(self, document_id: str, acl: AccessControlList) -> None:
        old_lookup = self._lookup(document_id)
        assert_user_has_access(old_lookup.acl, AccessLevel.WRITE, self.user)
        old_lookup.acl = acl
        self._update_lookup(old_lookup)

    def get_lookup(self, document_id: str) -> DocumentLookUp:
        lookup = self._lookup(document_id)
        assert_user_has_access(lookup.acl, AccessLevel.READ, self.user)
        return lookup

    def _remove_lookup(self, lookup_id):
        return self.acl_lookup_db.delete(f"{self.name}:{lookup_id}")

    def get(self, uid: str | UUID4) -> dict:
        uid = str(uid)
        lookup = self._lookup(uid)
        assert_user_has_access(lookup.acl, AccessLevel.READ, self.user)
        if cached_document := self.document_cache.get(f"{self.name}:{uid}"):
            return cached_document
        repo = self.repositories[lookup.repository]
        document = repo.get(uid)
        self.document_cache.set(f"{self.name}:{uid}", document, DOCUMENT_CACHE_TTL)
        return document

    # TODO: Implement find across repositories
    def find(self, filter: dict) -> list[dict]:
        repo = self.get_default_repository()

        documents_with_access: list[dict] = []
        for entity in repo.find(filter):
            if lookup := self._lookup(entity.get("_id")):
                try:
                    assert_user_has_access(lookup.acl, AccessLevel.READ, self.user)
                    documents_with_access.append(entity)
                except MissingPrivilegeException:
                    pass
        return documents_with_access

    @staticmethod
    def _assert_valid_name(document: dict) -> None:
        if (name := document.get("name")) and not url_safe_name(name):
            raise BadRequestException(
                f"'{name}' is a invalid document name. Only alphanumeric,"
                + " underscore, and dash are allowed characters"
            )

    def _parent_acl(self, parent_id: str | None) -> AccessControlList:
        """The access control list a new document inherits, the data source's own if it has no parent."""
        if parent_root_uid := parent_id.split(".")[0] if parent_id else None:
            try:  # If parent_id passed, try to get its lookup
                return self._lookup(parent_root_uid).acl
            except NotFoundException:  # The parent has not yet been created.
                pass
        return self.acl

    def _new_lookup(
        self, document_id: str, parent_acl: AccessControlList, storage_attribute: StorageAttribute = None
    ) -> DocumentLookUp:
        """Build the lookup a document that does not yet exist will be read and access checked by."""
        # Before inserting a new lookUp, check permissions on parent resource
        assert_user_has_access(parent_acl, AccessLevel.WRITE, self.user)
        repo = self._get_repo_from_storage_attribute(storage_attribute)
        return DocumentLookUp(
            lookup_id=document_id,
            repository=repo.name,
            database_id=document_id,
            acl=AccessControlList(
                owner=self.user.user_id,
                roles=parent_acl.roles,
                users=parent_acl.users,
                others=parent_acl.others,
            ),
            storage_affinity=StorageDataTypes.DEFAULT.value,
            meta={"created": f"{datetime.now()}"},
        )

    def _lookup_for_update(
        self, document: dict, storage_attribute: StorageAttribute = None, parent_id: str | None = None
    ) -> DocumentLookUp:
        """Find the lookup a document is written through, creating one if the document is new.

        Shared by 'update' and 'update_many' so that a document is named, given an id, and given an
        inherited access control list in one place, however many documents are being written.
        """
        self._assert_valid_name(document)
        document["_id"] = document.get("_id", str(uuid4()))  # Create _id if not yet created

        try:  # Get the documents lookup
            lookup = self._lookup(document["_id"])
        except NotFoundException:  # No lookup found --> Create a new document
            lookup = self._new_lookup(document["_id"], self._parent_acl(parent_id), storage_attribute)
            self._update_lookup(lookup)

        assert_user_has_access(lookup.acl, AccessLevel.WRITE, self.user)
        return lookup

    def update(
        self, document: dict, storage_attribute: StorageAttribute = None, parent_id: str | None = None, **kwargs
    ) -> None:
        """
        Create or update a document.
        :param document: A dict of the document to create or update.
        :param storage_attribute: Used to decide on repository when creating new document
        :param parent_id: Needed when adding a new child document that should inherit ACL.
        :return: None
        """
        lookup = self._lookup_for_update(document, storage_attribute, parent_id)
        self.repositories[lookup.repository].update(document["_id"], document)
        self.document_cache.set(f"{self.name}:{document['_id']}", document, DOCUMENT_CACHE_TTL)

    def _lookups(self, document_ids: list[str]) -> dict[str, DocumentLookUp]:
        """Read the lookups of many documents in one round trip. Documents that have none are left out."""
        values = self.acl_lookup_db.get_many([f"{self.name}:{document_id}" for document_id in document_ids])
        return {
            document_id: DocumentLookUp(**value)
            for document_id, value in zip(document_ids, values, strict=False)
            if value
        }

    def update_many(
        self, documents: list[dict], storage_attribute: StorageAttribute = None, parent_id: str | None = None
    ) -> None:
        """Create or update many documents, in a fixed number of round trips rather than one per document.

        See 'update' for a single document. Writing a document one at a time costs four round trips
        each: reading its lookup, writing its lookup, writing the document, and caching it. Eighty
        documents, the size of one package of an application import, therefore cost three hundred and
        twenty. Here every lookup is read at once, the new ones are written at once, the documents are
        written once per repository, and they are cached at once, which is four round trips whether
        there are eighty documents or eight hundred.
        """
        if not documents:
            return

        for document in documents:
            self._assert_valid_name(document)
            document["_id"] = document.get("_id", str(uuid4()))  # Create _id if not yet created

        document_ids = [document["_id"] for document in documents]
        lookups = self._lookups(document_ids)

        parent_acl: AccessControlList | None = None
        new_lookups: dict[str, dict] = {}
        for document_id in document_ids:
            if document_id in lookups:
                continue
            if parent_acl is None:  # Every document in a call shares a parent, so it is resolved once
                parent_acl = self._parent_acl(parent_id)
            lookups[document_id] = self._new_lookup(document_id, parent_acl, storage_attribute)
            new_lookups[f"{self.name}:{document_id}"] = lookups[document_id].dict()

        for document_id in document_ids:
            assert_user_has_access(lookups[document_id].acl, AccessLevel.WRITE, self.user)

        # Written before the documents, as the single document path does, so that a write which fails
        # part way cannot leave documents behind that have no lookup to read them by.
        self.acl_lookup_db.set_many(new_lookups)

        documents_per_repository: dict[str, list[dict]] = {}
        for document in documents:
            documents_per_repository.setdefault(lookups[document["_id"]].repository, []).append(document)

        for repository_name, repository_documents in documents_per_repository.items():
            self.repositories[repository_name].bulk_update(repository_documents)

        # Follows the repository write, as the single document path does, so that a reader which
        # missed just before the write cannot leave the body it read behind in the cache. Caching
        # what was written costs one round trip rather than one per document now, and the caller
        # that writes a package goes on to validate it, reading every document straight back; a
        # reader that misses pays a repository read and a cache write, so filling the cache here
        # costs less than leaving it empty for all but the largest package of an application.
        self.document_cache.set_many(
            {f"{self.name}:{document['_id']}": document for document in documents}, DOCUMENT_CACHE_TTL
        )

    def update_blob(self, uid: str, filename: str, content_type: str, file) -> None:
        repo = self._get_repo_from_storage_attribute(
            StorageAttribute(
                name="generic_blob",
                contained=False,
                storage_affinity=StorageDataTypes.BLOB,
            ),
            strict=True,
        )
        meta = {
            "created": f"{datetime.now()}",
            "filename": filename,
            "filetype": content_type,
        }
        lookup = DocumentLookUp(
            lookup_id=uid,
            repository=repo.name,
            database_id=uid,
            acl=AccessControlList.default_with_owner(self.user),
            storage_affinity=StorageDataTypes.BLOB.value,
            meta=meta,
        )
        assert_user_has_access(lookup.acl, AccessLevel.WRITE, self.user)
        self._update_lookup(lookup)
        repo.update_blob(uid, file.read())

    def get_blob(self, uid: str) -> bytes:
        lookup = self._lookup(uid)
        assert_user_has_access(lookup.acl, AccessLevel.READ, self.user)
        return self.repositories[lookup.repository].get_blob(lookup.database_id)

    def delete_blob(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            lookup = self._lookup(uid)
            assert_user_has_access(lookup.acl, AccessLevel.WRITE, self.user)
            self._remove_lookup(uid)
            self.repositories[lookup.repository].delete_blob(uid)
        except NotFoundException:
            logger.warning(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")

    def delete(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            lookup = self._lookup(uid)
            assert_user_has_access(lookup.acl, AccessLevel.WRITE, self.user)
            self._remove_lookup(uid)
            self.repositories[lookup.repository].delete(uid)
            self.document_cache.delete(f"{self.name}:{uid}")
        except NotFoundException:
            logger.warning(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")
