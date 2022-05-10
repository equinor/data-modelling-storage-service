from time import sleep
from typing import Dict, List, Optional

import gridfs
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, WriteError
from utils.encryption import decrypt

from storage.repository_interface import RepositoryInterface
from utils.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from utils.logging import logger
from utils.cosmos_rate_limit_handler import rate_limit_handler
from config import config
from utils.cosmos_rate_limit_handler import rate_limit_handler


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
            password=decrypt(password),
            tls=tls if tls or config.MONGO_SELF_SIGN_CA_CRT else False,
            tlsCAFile=config.MONGO_SELF_SIGN_CA_PATH if config.MONGO_SELF_SIGN_CA_CRT else None,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            retryWrites=False,
        )[database]
        self.blob_handler = gridfs.GridFS(self.handler)
        self.collection = collection

    @rate_limit_handler
    def get(self, uid: str) -> Dict:
        result = self.handler[self.collection].find_one(filter={"_id": uid})
        return result

    @rate_limit_handler
    def add(self, uid: str, document: Dict) -> bool:
        document["_id"] = uid
        try:
            return self.handler[self.collection].insert_one(document).acknowledged
        except DuplicateKeyError:
            raise EntityAlreadyExistsException

    @rate_limit_handler
    def update(self, uid: str, document: Dict) -> bool:
        return self.handler[self.collection].replace_one({"_id": uid}, document, upsert=True).acknowledged

    @rate_limit_handler
    def delete(self, uid: str) -> bool:
        return self.handler[self.collection].delete_one(filter={"_id": uid}).acknowledged

    @rate_limit_handler
    def find(self, filters: Dict) -> Optional[List[Dict]]:
        return self.handler[self.collection].find(filter=filters)

    @rate_limit_handler
    def find_one(self, filters: Dict) -> Optional[Dict]:
        return self.handler[self.collection].find_one(filter=filters)

    @rate_limit_handler
    def update_blob(self, uid: str, blob: bytearray):
        attempts = 0
        while True:
            try:
                attempts += 1
                response = self.blob_handler.put(blob, _id=uid)
                return response
            except WriteError as error:  # Likely caused by MongoDB rate limiting.
                logger.warning(f"Failed to upload blob (attempt: {attempts}), will retry:\n\t{error}")
                sleep(2)
                if attempts > 2:
                    raise error

    @rate_limit_handler
    def delete_blob(self, uid: str):
        return self.blob_handler.delete(uid)

    @rate_limit_handler
    def get_blob(self, uid: str) -> bytearray:
        blob = self.blob_handler.get(uid)
        if not blob:
            raise EntityNotFoundException(uid)
        return blob.read()
