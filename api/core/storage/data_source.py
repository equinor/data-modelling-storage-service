from typing import Dict, List, Union

from api.classes.document_look_up import DocumentLookUp
from api.classes.dto import DTO
from api.classes.repository import Repository
from api.config import Config
from api.core.storage.repository_exceptions import EntityNotFoundException
from api.services.database import dmt_database
from api.utils.logging import logger

data_source_collection = dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"]


# TODO: Make choices from StorageRecipe
class DataSource:
    def __init__(self, name: str, repositories):
        self.name = name
        self.repositories = repositories

    @classmethod
    def from_dict(cls, a_dict):
        return cls(a_dict["name"], {key: Repository(**value) for key, value in a_dict["repositories"].items()})

    def _get_repository(self, document_id) -> Repository:
        lookup = self.lookup(document_id)
        return self.repositories[lookup["repository"]]

    # TODO: Read default attribute from DataSource spec
    def _get_default_repository(self):
        return next(iter(self.repositories.values()))

    def lookup(self, document_id) -> Dict:
        res = data_source_collection.find_one(
            filter={"_id": self.name, f"documentLookUp.{document_id}.lookUpId": document_id},
            projection={f"documentLookUp.{document_id}": True},
        )
        if not res:
            raise EntityNotFoundException(document_id)
        return res["documentLookUp"][document_id]

    def insert_lookup(self, lookup: DocumentLookUp):
        res = data_source_collection.update_one(
            filter={"_id": self.name}, update={"$set": {f"documentLookUp.{lookup.lookup_id}": lookup.to_dict()}}
        )
        return res

    def remove_lookup(self, lookup_id):
        res = data_source_collection.update_one(
            filter={"_id": self.name}, update={"$unset": {f"documentLookUp.{lookup_id}": ""}}
        )
        return res

    def get(self, uid: str) -> DTO:
        repo = self._get_repository(uid)
        try:
            result = repo.get(uid)
            return DTO(result)
        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(f"the document with uid: {uid} was not found")

    # TODO: Implement find across repositories
    def find(self, filter: dict) -> Union[DTO, List[DTO]]:
        repo = self._get_default_repository()
        result = repo.find(filter)
        return [DTO(item) for item in result]

    # TODO: Deprecate this
    def first(self, filter: dict) -> Union[DTO, None]:
        repo = self._get_default_repository()
        result = repo.find_one(filter)
        if result:
            return DTO(result)

    def update(self, document: DTO) -> None:
        repo = self._get_repository(document.uid)
        if (
            not document.name == document.data["name"]
            or not document.type == document.data["type"]
            or not document.uid == document.data["_id"]
        ):
            raise ValueError("The meta data and tha 'data' object in the DTO does not match!")
        repo.update(document.uid, document.data)

    def add(self, document: DTO) -> None:
        repo = self._get_default_repository()
        self.insert_lookup(DocumentLookUp(document.uid, repo.name, document.uid, "", document.type))
        repo.add(document.uid, document.data)

    def delete(self, uid: str) -> None:
        repo = self._get_repository(uid)
        repo.delete(uid)
