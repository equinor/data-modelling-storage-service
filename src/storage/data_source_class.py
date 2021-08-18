from typing import Dict, List, Union

from pydantic import UUID4

from authentication.access_control import access_control, AccessLevel, ACL, create_acl
from domain_classes.document_look_up import DocumentLookUp
from domain_classes.dto import DTO
from domain_classes.repository import Repository
from domain_classes.storage_recipe import StorageAttribute
from enums import StorageDataTypes
from services.database import data_source_collection
from utils.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from utils.logging import logger


class DataSource:
    """
    A DataSource instance is an abstraction layer over several repositories(databases/storage backends).
    Access Control is done in the DataSource based on the Access Control Lists defined in the internal lookup tables.
    """

    def __init__(self, name: str, repositories, data_source_collection=data_source_collection):
        self.name = name
        self.repositories: Dict[str, Repository] = repositories
        self.data_source_collection = data_source_collection

    @classmethod
    def from_dict(cls, a_dict):
        return cls(
            a_dict["name"], {key: Repository(name=key, **value) for key, value in a_dict["repositories"].items()}
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

    def _get_documents_repository(self, document_id) -> Repository:
        lookup = self._lookup(document_id)
        return self.repositories[lookup.repository]

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

        raise EntityNotFoundException(document_id)

    def _update_lookup(self, lookup: DocumentLookUp):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$set": {f"documentLookUp.{lookup.lookup_id}": lookup.dict()}}
        )

    def update_access_control(self, document_id: str, acl: ACL) -> None:
        old_lookup = self._lookup(document_id)
        access_control(old_lookup.acl, AccessLevel.WRITE)
        old_lookup.acl = acl
        self._update_lookup(old_lookup)

    def get_access_control(self, document_id: str) -> DocumentLookUp:
        lookup = self._lookup(document_id)
        access_control(lookup.acl, AccessLevel.READ)
        return lookup

    def _remove_lookup(self, lookup_id):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$unset": {f"documentLookUp.{lookup_id}": ""}}
        )

    def get(self, uid: Union[str, UUID4]) -> DTO:
        uid = str(uid)
        try:
            lookup = self._lookup(uid)
            access_control(lookup.acl, AccessLevel.READ)
            repo = self.repositories[lookup.repository]
            return DTO(repo.get(uid))
        except EntityNotFoundException:
            raise EntityNotFoundException(
                uid, f"Document with id '{uid}' was not found in the '{self.name}' data-source"
            )

    # TODO: Implement find across repositories
    # TODO: Enable AccessControl
    def find(self, filter: dict) -> Union[DTO, List[DTO]]:
        repo = self.get_default_repository()
        result = repo.find(filter)
        return [DTO(item) for item in result]

    # TODO: Deprecate this
    # TODO: Enable AccessControl
    def first(self, filter: dict) -> Union[DTO, None]:
        repo = self.get_default_repository()
        result = repo.find_one(filter)
        if result:
            return DTO(result)

    def update(self, document: DTO, storage_attribute: StorageAttribute = None) -> None:
        # Since update() can also insert, we must check if it exists, and if not, insert a lookup
        try:
            lookup = self._lookup(document.uid)
            repo = self.repositories[lookup.repository]
        except EntityNotFoundException:
            repo = self._get_repo_from_storage_attribute(storage_attribute)
            lookup = DocumentLookUp(
                lookup_id=document.uid, repository=repo.name, database_id=document.uid, acl=create_acl()
            )
            self._update_lookup(lookup)

        if (
            not document.name == document.data["name"]
            or not document.type == document.data["type"]
            or not document.uid == document.data["_id"]
        ):
            raise ValueError("The metadata and tha 'data' object in the DTO does not match!")
        access_control(lookup.acl, AccessLevel.WRITE)
        repo.update(document.uid, document.data)

    # TODO: Ensure a root level restriction
    # No access control on the 'add' operation. Permissions are checked in parent.
    def add(self, document: DTO, storage_attribute: StorageAttribute = None) -> None:
        repo: Repository = self._get_repo_from_storage_attribute(storage_attribute)
        self._update_lookup(
            DocumentLookUp(lookup_id=document.uid, repository=repo.name, database_id=document.uid, acl=create_acl())
        )
        try:
            repo.add(document.uid, document.data)
        except EntityAlreadyExistsException:
            raise EntityAlreadyExistsException(
                message=f"The document with id '{document.uid}' already exist in data source '{self.name}'"
            )

    def update_blob(self, uid, file) -> None:
        repo = self._get_repo_from_storage_attribute(
            StorageAttribute("generic_blob", False, StorageDataTypes.BLOB.value), strict=True
        )
        lookup = DocumentLookUp(lookup_id=uid, repository=repo.name, database_id=uid, acl=create_acl())
        access_control(lookup.acl, AccessLevel.WRITE)
        self._update_lookup(lookup)
        repo.update_blob(uid, file.read())

    def get_blob(self, uid: str) -> bytes:
        lookup = self._lookup(uid)
        access_control(lookup.acl, AccessLevel.READ)
        return self.repositories[lookup.repository].get_blob(lookup.database_id)

    def delete(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            lookup = self._lookup(uid)
            access_control(lookup.acl, AccessLevel.WRITE)
            self._remove_lookup(uid)
            self.repositories[lookup.repository].delete(uid)
        except EntityNotFoundException:
            logger.warning(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")
            pass
