from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from api.core.storage.repository_interface import RepositoryInterface
from api.core.storage.repository_exceptions import EntityAlreadyExistsException
from typing import Dict, List, Optional


class MongoDBClient(RepositoryInterface):
    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        database: str = "data_modelling",
        collection: str = "data_modelling",
        tls: bool = False,
        port: int = 27001,
        **kwargs,
    ):
        self.handler = MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            tls=tls,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            retryWrites=False,
        )[database]
        self.collection = collection

    def get(self, uid: str) -> Dict:
        result = self.handler[self.collection].find_one(filter={"_id": uid})
        return result

    def add(self, uid: str, document: Dict) -> bool:
        document["_id"] = uid
        try:
            return self.handler[self.collection].insert_one(document).acknowledged
        except DuplicateKeyError:
            raise EntityAlreadyExistsException(document["id"])

    def update(self, uid: str, document: Dict) -> bool:
        try:
            # Update replaces the entire document in the database with the posted document
            return self.handler[self.collection].replace_one({"_id": uid}, document, upsert=True).acknowledged
        except Exception as error:
            print("ERROR", error)
            return False

    def delete(self, uid: str) -> bool:
        return self.handler[self.collection].delete_one(filter={"_id": uid}).acknowledged

    def find(self, filters: Dict) -> Optional[List[Dict]]:
        return self.handler[self.collection].find(filter=filters)

    def find_one(self, filters: Dict) -> Optional[Dict]:
        return self.handler[self.collection].find_one(filter=filters)
