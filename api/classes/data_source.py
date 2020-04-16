from typing import Dict

from api.core.enums import DataSourceType
from api.core.repository.azure.blob_repository import AzureBlobStorageClient

from api.core.repository.mongo import MongoDBClient
from flask import abort

from api.services.database import dmt_database as db


class DataSource:
    def __init__(self, data_source: Dict):
        self.name = data_source["name"]
        self.document_type = data_source["documentType"]
        self.data_source = data_source

    def get_client(self):
        data_source = self.data_source

        data_source_type = data_source["type"]

        if data_source_type == DataSourceType.MONGO.value:
            return MongoDBClient(
                host=data_source["host"],
                username=data_source["username"],
                password=data_source["password"],
                database=data_source["database"],
                tls=data_source.get("tls", False),
                collection=data_source["collection"],
                port=data_source["port"],
            )

        if data_source_type == DataSourceType.AZURE_BLOB_STORAGE.value:
            return AzureBlobStorageClient(
                account_name=data_source["account_name"],
                account_key=data_source["account_key"],
                collection=data_source["collection"],
            )


class DataSourceFactory:
    @staticmethod
    def _get_data_source_from_database(uid):
        data_source = db.data_sources.find_one({"_id": uid})
        if not data_source:
            abort(404, f"Error: The data-source was not found. ID: {uid}")
        return data_source

    def get_data_source(self, data_source_id):
        return DataSource(self._get_data_source_from_database(data_source_id))
