from typing import Dict, List, Optional

from api.core.enums import DataSourceType, StorageDataTypes
from api.core.storage.repositories.azure_blob import AzureBlobStorageClient
from api.core.storage.repositories.mongo import MongoDBClient
from api.core.storage.repository_interface import RepositoryInterface


class Repository(RepositoryInterface):
    def __init__(self, name, dataTypes: List[str] = None, **kwargs):
        self.name = name
        self.data_types = [StorageDataTypes(d) for d in dataTypes] if dataTypes else []
        self.client = self._get_client(**kwargs)

    def update(self, uid: str, document: Dict) -> bool:
        return self.client.update(uid, document)

    def get(self, uid: str) -> Dict:
        return self.client.get(uid)

    def delete(self, uid: str) -> bool:
        return self.client.delete(uid)

    def find(self, filters: Dict) -> Optional[List[Dict]]:
        return self.client.find(filters)

    def find_one(self, filters: Dict) -> Dict:
        return self.client.find_one(filters)

    def add(self, uid: str, document: Dict) -> bool:
        return self.client.add(uid, document)

    @staticmethod
    def _get_client(**kwargs):

        if kwargs["type"] == DataSourceType.MONGO.value:
            return MongoDBClient(**kwargs)

        if kwargs["type"] == DataSourceType.AZURE_BLOB_STORAGE.value:
            return AzureBlobStorageClient(**kwargs)
