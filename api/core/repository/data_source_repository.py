from typing import List, Dict

from api.config import Config
from api.services.database import dmt_database
from api.core.enums import DataSourceDocumentType, DataSourceType


class DataSourceRepository:
    collection = dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"]

    def list(self, document_type: DataSourceDocumentType) -> List[Dict]:
        all_sources = [
            {"id": "local", "host": "client", "name": "Local workspace", "type": DataSourceType.LOCAL.value}
        ]
        for data_source in self.collection.find(
            filter={"documentType": {"$regex": document_type.value}}, projection=["name", "host", "type"]
        ):
            data_source["id"] = data_source.pop("_id")

            data_source_type = DataSourceType(data_source["type"])

            if data_source_type == DataSourceType.MONGO:
                all_sources.append(
                    {
                        "id": data_source["id"],
                        "host": data_source["host"],
                        "name": data_source["name"],
                        "type": data_source_type.value,
                    }
                )
            if data_source_type == DataSourceType.AZURE_BLOB_STORAGE:
                # TODO: Remove host?
                all_sources.append(
                    {"id": data_source["id"], "name": data_source["name"], "type": data_source_type.value, "host": ""}
                )

        return all_sources

    def create(self, id: str, document):
        document["_id"] = id
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
