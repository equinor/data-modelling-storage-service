from typing import List, Dict

from api.core.storage.repository_exceptions import DataSourceNotFoundException

from api.config import Config
from api.core.storage.data_source import DataSource
from api.request_types.create_data_source import DataSourceRequest
from api.services.database import dmt_database
from api.core.enums import DataSourceType


class DataSourceRepository:
    collection = dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"]

    def list(self) -> List[Dict]:
        all_sources = [
            {"id": "local", "host": "client", "name": "Local workspace", "type": DataSourceType.LOCAL.value}
        ]
        for data_source in self.collection.find(projection={"name"}):
            data_source["id"] = data_source.pop("_id")
            all_sources.append({"id": data_source["id"], "name": data_source["name"]})

        return all_sources

    def create(self, id: str, document: DataSourceRequest):
        document = document.dict()
        document["_id"] = id
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get(self, id: str):
        data_source = self.collection.find_one(filter={"_id": id})
        if not data_source:
            raise DataSourceNotFoundException(id)
        return DataSource.from_dict(data_source)


def get_data_source(data_source_id: str) -> DataSource:
    return DataSourceRepository().get(data_source_id)
