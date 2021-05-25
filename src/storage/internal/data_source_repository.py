from typing import List, Dict

from pymongo.errors import DuplicateKeyError

from config import Config
from services.database import dmt_database
from restful.request_types.create_data_source import DataSourceRequest
from storage.data_source_class import DataSource
from utils.exceptions import DataSourceAlreadyExistsException, DataSourceNotFoundException, InvalidEntityException
from utils.logging import logger


class DataSourceRepository:
    collection = dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"]

    # TODO
    @staticmethod
    def validate_data_source(document: dict):
        pass

    def list(self) -> List[Dict]:
        all_sources = []
        for data_source in self.collection.find(projection={"name"}):
            data_source["id"] = data_source.pop("_id")
            all_sources.append({"id": data_source["id"], "name": data_source["name"]})

        return all_sources

    def create(self, id: str, document: DataSourceRequest):
        document = document.dict()
        document["_id"] = id
        try:
            self.validate_data_source(document)
            result = self.collection.insert_one(document)
        except InvalidEntityException:
            raise InvalidEntityException(f"Failed to create data source '{id}'. The posted entity is invalid...")
        except DuplicateKeyError:
            logger.warning(f"Tried to create a datasource that already exists ('{id}')")
            raise DataSourceAlreadyExistsException(id)
        return str(result.inserted_id)

    def get(self, id: str) -> DataSource:
        data_source = self.collection.find_one(filter={"_id": id})
        if not data_source:
            raise DataSourceNotFoundException(id)
        return DataSource.from_dict(data_source)


def get_data_source(data_source_id: str) -> DataSource:
    return DataSourceRepository().get(data_source_id)
