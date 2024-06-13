import json
from time import sleep

import gridfs
from pymongo import MongoClient
from pymongo.errors import OperationFailure, WriteError

from common.exceptions import BadRequestException, NotFoundException
from common.utils.encryption import decrypt, encrypt
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
        self.encrypt_at_rest = kwargs.get("encryptAtRest", False)

    def _decrypt_document(self, document: dict | list[dict]) -> dict:
        if isinstance(document, list):
            return [json.loads(decrypt(doc["data"])) for doc in document]
        return json.loads(decrypt(document["data"]))

    def _encrypt_document(self, document: dict | list[dict]) -> dict:
        if isinstance(document, list):
            return [{"_id": doc["_id"], "data": encrypt(json.dumps(doc))} for doc in document]
        return {"_id": document["_id"], "data": encrypt(json.dumps(document))}

    def get(self, uid: str) -> dict:
        attempts = 0
        while attempts < 50:
            attempts += 1
            try:
                doc = self.handler[self.collection].find_one(filter={"_id": uid})
                if self.encrypt_at_rest:
                    return self._decrypt_document(doc)
                return doc
            except (WriteError, OperationFailure) as ex:
                sleep(3)
                if attempts > 2:
                    raise ex
        raise NotFoundException(uid)

    def update(self, uid: str, document: dict, **kwargs) -> bool:
        attempts = 0
        while attempts < 50:
            attempts += 1
            try:
                if self.encrypt_at_rest:
                    document = self._encrypt_document(document)
                return self.handler[self.collection].replace_one({"_id": uid}, document, upsert=True).acknowledged
            except (WriteError, OperationFailure) as ex:
                sleep(3)
                if attempts > 2:
                    raise ex
        raise NotFoundException(uid)

    def delete(self, uid: str) -> bool:
        return self.handler[self.collection].delete_one(filter={"_id": uid}).acknowledged

    def find(self, filters: dict) -> list[dict] | None:
        doc = self.handler[self.collection].find(filter=filters)
        if self.encrypt_at_rest and doc:
            return self._decrypt_document(doc)
        return doc

    def find_one(self, filters: dict) -> dict | None:
        doc = self.handler[self.collection].find_one(filter=filters)
        if self.encrypt_at_rest and doc:
            return self._decrypt_document(doc)

    def update_blob(self, uid: str, blob: bytearray):
        if self.encrypt_at_rest:
            raise NotImplementedError("Blob encryption is not supported")
        attempts = 0
        while attempts < 50:
            try:
                attempts += 1
                response = self.blob_handler.put(blob, _id=uid)
                return response
            except (WriteError, OperationFailure) as error:  # Likely caused by MongoDB rate limiting.
                logger.warning(f"Failed to upload blob (attempt: {attempts}), will retry:\n\t{error}")
                sleep(3)
                if attempts > 2:
                    raise error
            except gridfs.errors.FileExists as ex:
                if attempts > 1:  # The blob was actually added, even if we got 429...
                    return
                message = f"Blob file with id '{uid}' already exists"
                logger.warning(message)
                raise BadRequestException(message=message) from ex

    def delete_blob(self, uid: str):
        return self.blob_handler.delete(uid)

    def get_blob(self, uid: str) -> bytearray:
        if self.encrypt_at_rest:
            raise NotImplementedError("Blob encryption is not supported")
        blob = self.blob_handler.get(uid)
        if not blob:
            raise NotFoundException(uid)
        return blob.read()
