import json
from typing import Optional

from azure.storage.blob import BlobServiceClient

from common.utils.encryption import decrypt
from storage.repository_interface import RepositoryInterface


class AzureBlobStorageClient(RepositoryInterface):
    def __init__(self, account_url: str, container: str, **kwargs):
        blob_service_client = BlobServiceClient(account_url=decrypt(account_url))
        self.blob_service_client = blob_service_client
        self.container = container

    def get(self, uid: str) -> dict:
        result = self.blob_service_client.get_blob_to_text(self.container, uid)
        document = json.loads(result.content)
        document["_id"] = uid
        return document

    def add(self, uid: str, document: dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.container, uid, output)
        return True

    def update_blob(self, uid: str, blob: bytearray):
        self.blob_service_client.create_blob_from_bytes(self.container, uid, blob)

    def get_blob(self, uid: str) -> bytearray:
        return self.blob_service_client.get_blob_to_bytes(self.container, uid).content

    def update(self, uid: str, document: dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.container, uid, output)
        return True

    def delete(self, uid: str) -> bool:
        self.blob_service_client.delete_blob(self.container, uid)
        return True

    def delete_blob(self, uid: str) -> bool:
        self.delete(uid)
        return True

    def find(self, filters: dict) -> Optional[list[dict]]:
        # TODO: implement efficient filter functionality by using the python azure src
        if self.blob_service_client.exists(self.container):
            # self.blob_service_client.create_container(self.collection)
            blobs = self.blob_service_client.list_blobs(self.container)
            result = self._filter(blobs, filters)
            return result
        return None

    def find_one(self, filters: dict) -> Optional[dict]:
        blobs = self.blob_service_client.list_blobs(self.container)
        result = self._filter(blobs, filters)
        if len(result) > 0:
            return result[0]
        return None

    def _filter(self, blobs, filters) -> list[dict]:
        result = []
        for blob in blobs:
            document = self.get(str(blob.name))
            for key, value in filters.items():
                if key not in document or document[key] != value:
                    continue
                else:
                    result.append(document)
        return result
