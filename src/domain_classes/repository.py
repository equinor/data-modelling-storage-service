from functools import lru_cache
from typing import Optional

from config import config
from enums import RepositoryType, StorageDataTypes
from storage.repositories.azure_blob import AzureBlobStorageClient
from storage.repositories.mongo import MongoDBClient
from storage.repository_interface import RepositoryInterface


class Repository(RepositoryInterface):
    def __init__(self, name, data_types: list[str] = None, **kwargs):
        self.name = name
        self.data_types = [StorageDataTypes(d) for d in data_types] if data_types else []
        self.client = self._get_client(**kwargs)

    def update(self, uid: str, document: dict) -> bool:
        return self.client.update(uid, document)

    def get(self, uid: str) -> dict:
        return self.client.get(uid)

    def delete(self, uid: str) -> bool:
        return self.client.delete(uid)

    def delete_blob(self, uid: str) -> bool:
        return self.client.delete_blob(uid)

    def find(self, filters: dict) -> Optional[list[dict]]:
        return self.client.find(filters)

    def find_one(self, filters: dict) -> dict:
        return self.client.find_one(filters)

    def add(self, uid: str, document: dict) -> bool:
        return self.client.add(uid, document)

    def update_blob(self, uid: str, blob: bytes) -> bool:
        return self.client.update_blob(uid, blob)

    def get_blob(self, uid: str) -> bytes:
        return self.client.get_blob(uid)

    @staticmethod
    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def _get_client(**kwargs):
        if kwargs["type"] == RepositoryType.MONGO.value:
            return MongoDBClient(**kwargs)

        if kwargs["type"] == RepositoryType.AZURE_BLOB_STORAGE.value:
            return AzureBlobStorageClient(**kwargs)
