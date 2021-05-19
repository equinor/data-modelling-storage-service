from typing import Dict, List, Union

from pydantic import UUID4

from config import Config
from domain_classes.document_look_up import DocumentLookUp
from domain_classes.dto import DTO
from domain_classes.repository import Repository
from domain_classes.storage_recipe import StorageAttribute
from enums import StorageDataTypes
from services.database import dmt_database
from utils.exceptions import EntityNotFoundException
from utils.logging import logger


class DataSource:
    def __init__(self, name: str, repositories, data_source_collection=None):
        self.name = name
        self.repositories: Dict[Repository] = repositories
        self.data_source_collection = (
            data_source_collection if data_source_collection else dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"]
        )

    @classmethod
    def from_dict(cls, a_dict):
        return cls(a_dict["name"], {key: Repository(**value) for key, value in a_dict["repositories"].items()})

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
        lookup = self.lookup(document_id)
        return self.repositories[lookup["repository"]]

    # TODO: Read default attribute from DataSource spec
    def get_default_repository(self) -> Repository:
        # Now just returns the first repo in the ordered_dict
        return next(iter(self.repositories.values()))

    def lookup(self, document_id) -> Dict:
        res = self.data_source_collection.find_one(
            filter={"_id": self.name, f"documentLookUp.{document_id}.lookUpId": document_id},
            projection={f"documentLookUp.{document_id}": True},
        )
        if not res:
            raise EntityNotFoundException(document_id)
        return res["documentLookUp"][document_id]

    def insert_lookup(self, lookup: DocumentLookUp):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$set": {f"documentLookUp.{lookup.lookup_id}": lookup.to_dict()}}
        )

    def remove_lookup(self, lookup_id):
        return self.data_source_collection.update_one(
            filter={"_id": self.name}, update={"$unset": {f"documentLookUp.{lookup_id}": ""}}
        )

    def get(self, uid: Union[str, UUID4]) -> DTO:
        uid = str(uid)
        try:
            lookup = self.lookup(uid)
            repo = self.repositories[lookup["repository"]]
            return DTO(repo.get(uid))
        except EntityNotFoundException:
            raise EntityNotFoundException(f"{uid} was not found in the '{self.name}' data-sources lookupTable")
        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(f"Unknown error on fetching the document with uid: {uid} was not found")

    # TODO: Implement find across repositories
    def find(self, filter: dict) -> Union[DTO, List[DTO]]:
        repo = self.get_default_repository()
        result = repo.find(filter)
        return [DTO(item) for item in result]

    # TODO: Deprecate this
    def first(self, filter: dict) -> Union[DTO, None]:
        repo = self.get_default_repository()
        result = repo.find_one(filter)
        if result:
            return DTO(result)

    def update(self, document: DTO, storage_attribute: StorageAttribute = None) -> None:
        # Since update() can also insert, we must check if it exists, and if not, insert a lookup
        try:
            repo = self._get_documents_repository(document.uid)
        except EntityNotFoundException:
            repo = self._get_repo_from_storage_attribute(storage_attribute)
            self.insert_lookup(DocumentLookUp(document.uid, repo.name, document.uid, "", document.type))

        if (
            not document.name == document.data["name"]
            or not document.type == document.data["type"]
            or not document.uid == document.data["_id"]
        ):
            raise ValueError("The meta data and tha 'data' object in the DTO does not match!")
        repo.update(document.uid, document.data)

    def add(self, document: DTO, storage_attribute: StorageAttribute = None) -> None:
        repo = self._get_repo_from_storage_attribute(storage_attribute)
        self.insert_lookup(DocumentLookUp(document.uid, repo.name, document.uid, "", document.type))
        repo.add(document.uid, document.data)

    def update_blob(self, uid, file) -> None:
        repo = self._get_repo_from_storage_attribute(
            StorageAttribute("generic_blob", False, StorageDataTypes.BLOB.value), strict=True
        )
        self.insert_lookup(DocumentLookUp(uid, repo.name, uid, "", "blob"))
        # TODO: Some sanity checks on the file. werkzug safe_files() etc.
        repo.update_blob(uid, file.read())

    def get_blob(self, uid: str) -> bytes:
        try:
            repo = self._get_documents_repository(uid)
            if not repo:
                logger.error(f"{uid} was not found in the '{self.name}' data-sources lookupTable")
                raise EntityNotFoundException(f"{uid} was not found in the '{self.name}' data-sources lookupTable")

            return repo.get_blob(uid)

        except EntityNotFoundException:
            logger.error(f"{uid} was not found in the '{self.name}' data-sources lookupTable")
            raise EntityNotFoundException(f"{uid} was not found in the '{self.name}' data-sources lookupTable")

        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(f"The blob with uid: {uid} was not found")

    def delete(self, uid: str) -> None:
        # If lookup not found, assume it's deleted
        try:
            repo = self._get_documents_repository(uid)
            self.remove_lookup(uid)
            repo.delete(uid)
        except EntityNotFoundException:
            logger.warn(f"Failed trying to delete entity with uid '{uid}'. Could not be found in lookup table")
            pass
