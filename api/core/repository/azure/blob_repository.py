from api.core.repository.db_client_interface import DBClientInterface
from azure.storage.blob.blockblobservice import BlockBlobService
from typing import Dict, List, Optional
import json


class AzureBlobStorageClient(DBClientInterface):
    def __init__(self, account_name: str, account_key: str, collection: str):
        blob_service_client = BlockBlobService(account_name=account_name, account_key=account_key)
        self.blob_service_client = blob_service_client
        self.collection = collection

    def get(self, uid: str) -> Dict:
        result = self.blob_service_client.get_blob_to_text(self.collection, uid)
        document = json.loads(result.content)
        document["_id"] = uid
        return document

    def add(self, uid: str, document: Dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.collection, uid, output)

    def update(self, uid: str, document: Dict) -> bool:
        output = json.dumps(document)
        self.blob_service_client.create_blob_from_text(self.collection, uid, output)

    def delete(self, uid: str) -> bool:
        self.blob_service_client.delete_blob(self.collection, uid)

    def find(self, filters: Dict) -> Optional[List[Dict]]:
        # TODO: implement efficient filter functionality by using the python azure api
        blobs = self.blob_service_client.list_blobs(self.collection)
        result = self._filter(blobs, filters)
        return result

    def find_one(self, filters: Dict) -> Optional[Dict]:
        blobs = self.blob_service_client.list_blobs(self.collection)
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
