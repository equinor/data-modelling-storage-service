from typing import List, Union

from api.classes.dto import DTO
from api.core.repository.db_client_interface import DBClientInterface
from api.core.repository.repository_exceptions import EntityNotFoundException
from api.utils.logging import logger


class Repository:
    def __init__(self, name: str, db: DBClientInterface):
        self.name = name
        self.client = db

    def get(self, uid: str) -> DTO:
        try:
            result = self.client.get(uid)
            return DTO(result)
        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(f"the document with uid: {uid} was not found")

    def find(self, filter: dict) -> Union[DTO, List[DTO]]:
        result = self.client.find(filter)
        return [DTO(item) for item in result]

    def first(self, filter: dict) -> Union[DTO, None]:
        result = self.client.find_one(filter)
        if result:
            return DTO(result)

    def update(self, document: DTO) -> None:
        if (
            not document.name == document.data["name"]
            or not document.type == document.data["type"]
            or not document.uid == document.data["_id"]
        ):
            raise ValueError("The meta data and tha 'data' object in the DTO does not match!")
        self.client.update(document.uid, document.data)

    def add(self, document: DTO) -> None:
        self.client.add(document.uid, document.data)

    def delete(self, uid: str) -> None:
        self.client.delete(uid)
