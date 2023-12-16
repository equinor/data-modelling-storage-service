from time import sleep

import gridfs
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure, WriteError

from common.exceptions import BadRequestException, NotFoundException
from common.utils.encryption import decrypt
from common.utils.logging import logger
from storage.repository_interface import RepositoryInterface


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
            tls=tls,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            retryWrites=False,
        )[database]
        self.blob_handler = gridfs.GridFS(self.handler)
        self.collection = collection

    def get(self, uid: str) -> dict:
        attempts = 0
        while attempts < 50:
            attempts += 1
            try:
                return self.handler[self.collection].find_one(filter={"_id": uid})
            except (WriteError, OperationFailure) as ex:
                sleep(3)
                if attempts > 2:
                    raise ex
        raise NotFoundException(uid)

    def add(self, uid: str, document: dict) -> bool:
        document["_id"] = uid
        try:
            return self.handler[self.collection].insert_one(document).acknowledged
        except DuplicateKeyError as ex:
            raise BadRequestException from ex

    def update(self, uid: str, document: dict, **kwargs) -> bool:
        attempts = 0
        max_sleep_time = 30  # Maximum sleep time in seconds
        while attempts < 50:
            attempts += 1
            try:
                return self.handler[self.collection].replace_one({"_id": uid}, document, upsert=True).acknowledged
            except (WriteError, OperationFailure) as ex:
                sleep_time = min(2**attempts, max_sleep_time)
                sleep(sleep_time)
                if attempts >= 6:
                    logger.debug("Retries exceeded, raising error")
                    raise ex
        raise NotFoundException(uid)

    def delete(self, uid: str) -> bool:
        return self.handler[self.collection].delete_one(filter={"_id": uid}).acknowledged

    def find(self, filters: dict) -> list[dict] | None:
        return self.handler[self.collection].find(filter=filters)

    def find_one(self, filters: dict) -> dict | None:
        return self.handler[self.collection].find_one(filter=filters)

    def update_blob(self, uid: str, blob: bytearray):
        attempts = 0
        max_sleep_time = 30  # Maximum sleep time in seconds
        while attempts < 50:
            try:
                attempts += 1
                response = self.blob_handler.put(blob, _id=uid)
                return response
            except (WriteError, OperationFailure) as error:  # Likely caused by MongoDB rate limiting.
                logger.warning(f"Failed to upload blob (attempt: {attempts}), will retry:\n\t{error}")
                sleep_time = min(2**attempts, max_sleep_time)
                sleep(sleep_time)
                if attempts >= 6:
                    raise error
            except gridfs.errors.FileExists as ex:
                if attempts > 1:  # The blob was actually added, even if we got 429...
                    logger.info("Blob was added, even if we got 429")
                    return
                message = f"Blob file with id '{uid}' already exists"
                logger.warning(message)
                raise BadRequestException(message=message) from ex

    def delete_blob(self, uid: str):
        return self.blob_handler.delete(uid)

    def get_blob(self, uid: str) -> bytearray:
        blob = self.blob_handler.get(uid)
        if not blob:
            raise NotFoundException(uid)
        return blob.read()
