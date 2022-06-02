from typing import Dict, List, Optional

from enums import RepositoryType, StorageDataTypes
from storage.repositories.azure_blob import AzureBlobStorageClient
from storage.repositories.mongo import MongoDBClient
from storage.repository_interface import RepositoryInterface

from services.database import get_client


class Repository(RepositoryInterface):
    def __init__(self, name, data_types: List[str] = None, **kwargs):
        self.name = name
        self.data_types = [StorageDataTypes(d) for d in data_types] if data_types else []
        self.client = get_client(**kwargs)

    def update(self, uid: str, document: Dict) -> bool:
        return self.client.update(uid, document)

    def get(self, uid: str) -> Dict:
        return self.client.get(uid)

    def delete(self, uid: str) -> bool:
        return self.client.delete(uid)

    def delete_blob(self, uid: str) -> bool:
        return self.client.delete_blob(uid)

    def find(self, filters: Dict) -> Optional[List[Dict]]:
        return self.client.find(filters)

    def find_one(self, filters: Dict) -> Dict:
        return self.client.find_one(filters)

    def add(self, uid: str, document: Dict) -> bool:
        return self.client.add(uid, document)

    def update_blob(self, uid: str, blob: bytes) -> bool:
        return self.client.update_blob(uid, blob)

    def get_blob(self, uid: str) -> bytes:
        return self.client.get_blob(uid)

