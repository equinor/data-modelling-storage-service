from azure.storage.blob import BlobServiceClient
from typing import Dict, List, Optional
import json

from storage.repository_interface import RepositoryInterface
from utils.encryption import decrypt


class AzureBlobStorageClient(RepositoryInterface):
    def __init__(self, account_url: str, container: str, **kwargs):
        blob_service_client = BlobServiceClient(account_url=decrypt(account_url))
        self.blob_service_client = blob_service_client
        self.container = container

    def get(self, uid: str) -> Dict:
        result = self.blob_service_client.get_blob_to_text(self.container, uid)
        document = json.loads(result.content)
        document["_id"] = uid
        return document

    def add(self, uid: str, document: Dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.container, uid, output)

    def update_blob(self, uid: str, blob: bytearray):
        self.blob_service_client.create_blob_from_bytes(self.container, uid, blob)

    def get_blob(self, uid: str) -> bytearray:
        return self.blob_service_client.get_blob_to_bytes(self.container, uid).content

    def update(self, uid: str, document: Dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.container, uid, output)

    def delete(self, uid: str) -> bool:
        self.blob_service_client.delete_blob(self.container, uid)

    def delete_blob(self, uid: str) -> bool:
        self.delete(uid)

    def find(self, filters: Dict) -> Optional[List[Dict]]:
        # TODO: implement efficient filter functionality by using the python azure src
        if self.blob_service_client.exists(self.container):
            # self.blob_service_client.create_container(self.collection)
            blobs = self.blob_service_client.list_blobs(self.container)
            result = self._filter(blobs, filters)
            return result

    def find_one(self, filters: Dict) -> Optional[Dict]:
        blobs = self.blob_service_client.list_blobs(self.container)
        result = self._filter(blobs, filters)
        if len(result) > 0:
            return result[0]
        return None

    def _filter(self, blobs, filters) -> List[Dict]:
        result = {}
        for blob in blobs:
            document = self.get(str(blob.name))
            for key, value in filters.items():
                if key not in document or document[key] != value:
                    continue
                else:
                    result[document["_id"]] = document
        return result.values()
