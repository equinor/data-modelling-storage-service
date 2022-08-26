from typing import Dict, List, Union
from uuid import uuid4

from pydantic import UUID4
from common.utils.string_helpers import url_safe_name

from authentication.access_control import access_control, create_acl, DEFAULT_ACL
from authentication.models import AccessLevel, ACL, User
from domain_classes.document_look_up import DocumentLookUp
from domain_classes.repository import Repository
from domain_classes.storage_recipe import StorageAttribute
from enums import StorageDataTypes
from services.database import data_source_collection
from common.exceptions import NotFoundException, BadRequestException, MissingPrivilegeException,  NotFoundException
from common.utils.logging import logger


class DataSource:
    """
    A DataSource instance is an abstraction layer over several repositories(databases/storage backends).
    Access Control is done in the DataSource based on the Access Control Lists defined in the internal lookup tables.
    """

    def __init__(
        self,
        name: str,
        user: User,
        acl: ACL = DEFAULT_ACL,
        repositories=None,
        data_source_collection=data_source_collection,
    ):
        self.name = name
        self.user = user
        # This ACL is used when there is no parent to inherit ACL from. Controls who can create root-packages.
        self.acl = acl
        self.repositories: Dict[str, Repository] = repositories
        self.data_source_collection = data_source_collection

    @classmethod
    def from_dict(cls, a_dict, user: User):
        return cls(
            a_dict["name"],
            user,
            ACL(**a_dict.get("acl", DEFAULT_ACL.dict())),
            {key: Repository(name=key, **value) for key, value in a_dict["repositories"].items()},
        )

    def _get_repo_from_storage_attribute(self, storage_attribute: StorageAttribute = None, strict=False) -> Repository:
        # Not too smart yet...
        # Returns the first repo with a matching "dataType" value, or the first Repo if no match
        if storage_attribute:
            for r in self.repositories.values():
                if storage_attribute.storage_type_affinity in r.data_types:
                    return r
        if strict:
            raise ValueError(f"No repository for '{storage_attribute.storage_type_affinity}' data configured")
        return self.get_default_repository()

    # TODO: Read default attribute from DataSource spec
    def get_default_repository(self) -> Repository:
        # Now just returns the first repo in the ordered_dict
        return next(iter(self.repositories.values()))

    def _lookup(self, document_id) -> DocumentLookUp:
        if res := self.data_source_collection.find_one(
            filter={"_id": self.name, f"documentLookUp.{document_id}.lookup_id": document_id},
            projection={f"documentLookUp.{document_id}": True},
        ):
            return DocumentLookUp(**res["documentLookUp"][document_id])

        raise NotFoundException(message=f"Document with id '{document_id}' was not found in the '{self.name}' data-source")

    def _update_lookup(self, lookup: DocumentLookUp):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$set": {f"documentLookUp.{lookup.lookup_id}": lookup.dict()}}
        )

    def update_access_control(self, document_id: str, acl: ACL) -> None:
        old_lookup = self._lookup(document_id)
        access_control(old_lookup.acl, AccessLevel.WRITE, self.user)
        old_lookup.acl = acl
        self._update_lookup(old_lookup)

    def get_access_control(self, document_id: str) -> DocumentLookUp:
        lookup = self._lookup(document_id)
        access_control(lookup.acl, AccessLevel.READ, self.user)
        return lookup

    def _remove_lookup(self, lookup_id):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$unset": {f"documentLookUp.{lookup_id}": ""}}
        )

    def get(self, uid: Union[str, UUID4]) -> dict:
        uid = str(uid)
        lookup = self._lookup(uid)
        access_control(lookup.acl, AccessLevel.READ, self.user)
        repo = self.repositories[lookup.repository]
        return repo.get(uid)

    # TODO: Implement find across repositories
    def find(self, filter: dict) -> Union[dict, List[dict]]:
        repo = self.get_default_repository()

        documents_with_access: List[dict] = []
        for entity in repo.find(filter):
            if lookup := self._lookup(entity.get("_id")):
                try:
                    access_control(lookup.acl, AccessLevel.READ, self.user)
                    documents_with_access.append(entity)
                except MissingPrivilegeException:
                    pass
        return documents_with_access

    def update(self, document: dict, storage_attribute: StorageAttribute = None, parent_id: str = None) -> None:
        """
        Create or update a document.
        :param document: A dict of the document to create or update.
        :param storage_attribute: Used to decide on repository when creating new document
        :param parent_id: Needed when adding a new child document that should inherit ACL.
        :return: None
        """
        if name := document.get("name"):
            if not url_safe_name(name):
                raise BadRequestException(
                    f"'{name}' is a invalid document name. Only alphanumeric, underscore, and dash are allowed characters")

        document["_id"] = document.get("_id", str(uuid4()))  # Create _id if not yet created

        try:  # Get the documents lookup
            lookup = self._lookup(document["_id"])
        except NotFoundException:  # No lookup found --> Create a new document
            parent_lookup = None

            if parent_root_uid := parent_id.split(".")[0] if parent_id else None:
                try:  # If parent_id passed, try to get it's lookup
                    parent_lookup = self._lookup(parent_root_uid)
                except NotFoundException:  # The parent has not yet been created.
                    pass

            parent_acl = parent_lookup.acl if parent_lookup else self.acl  # If no parentLookup, use DataSource default
            # Before inserting a new lookUp, check permissions on parent resource
            access_control(parent_acl, AccessLevel.WRITE, self.user)
            repo = self._get_repo_from_storage_attribute(storage_attribute)
            document_owner = self.user
            acl: ACL = ACL(
                owner=document_owner.user_id,
                roles=parent_acl.roles,
                users=parent_acl.users,
                others=parent_acl.others,
            )
            lookup = DocumentLookUp(
                lookup_id=document["_id"], repository=repo.name, database_id=document["_id"], acl=acl
            )
            self._update_lookup(lookup)

        repo = self.repositories[lookup.repository]
        access_control(lookup.acl, AccessLevel.WRITE, self.user)
        repo.update(document["_id"], document)

    def update_blob(self, uid, file) -> None:
        repo = self._get_repo_from_storage_attribute(
            StorageAttribute("generic_blob", False, StorageDataTypes.BLOB.value), strict=True
        )
        lookup = DocumentLookUp(lookup_id=uid, repository=repo.name, database_id=uid, acl=create_acl(self.user))
        access_control(lookup.acl, AccessLevel.WRITE, self.user)
        self._update_lookup(lookup)
        repo.update_blob(uid, file.read())

    def get_blob(self, uid: str) -> bytes:
        lookup = self._lookup(uid)
        access_control(lookup.acl, AccessLevel.READ, self.user)
        return self.repositories[lookup.repository].get_blob(lookup.database_id)

    def delete_blob(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            lookup = self._lookup(uid)
            access_control(lookup.acl, AccessLevel.WRITE, self.user)
            self._remove_lookup(uid)
            self.repositories[lookup.repository].delete_blob(uid)
        except NotFoundException:
            logger.warning(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")
            pass

    def delete(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            lookup = self._lookup(uid)
            access_control(lookup.acl, AccessLevel.WRITE, self.user)
            self._remove_lookup(uid)
            self.repositories[lookup.repository].delete(uid)
        except NotFoundException:
            logger.warning(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")
            pass
