from typing import List, Dict

from pymongo.errors import DuplicateKeyError

from enums import RepositoryType
from services.database import data_source_collection
from restful.request_types.create_data_source import DataSourceRequest
from storage.data_source_class import DataSource
from utils.exceptions import (
    DataSourceAlreadyExistsException,
    DataSourceNotFoundException,
    InvalidDataSourceException,
    InvalidEntityException,
)
from utils.logging import logger

RESERVED_MONGO_DATABASES = ("admin", "local", "data-source-database")


class DataSourceRepository:
    @staticmethod
    def validate_data_source(document: dict):
        try:
            for repo in document["repositories"].values():
                if repo.get("name"):
                    raise InvalidDataSourceException("A repository specification may not have the 'name' key.")
                if repo["type"] == RepositoryType.MONGO.value:
                    if repo["database"] in RESERVED_MONGO_DATABASES:
                        raise InvalidDataSourceException(
                            f"The database named '{repo['database']}' " "is a system reserved database name."
                        )
        except KeyError as e:
            raise KeyError(e)
        except Exception as error:
            raise InvalidDataSourceException(error)

    @staticmethod
    def validate_repository(repo: dict):
        try:
            if repo.get("name"):
                raise InvalidDataSourceException("A repository specification may not have the 'name' key.")
            if repo["type"] == RepositoryType.MONGO.value:
                if repo["database"] in RESERVED_MONGO_DATABASES:
                    raise InvalidDataSourceException(
                        f"The database named '{repo['database']}' " "is a system reserved database name."
                    )
        except KeyError as e:
            raise KeyError(e)
        except Exception as error:
            raise InvalidDataSourceException(error)

    def list(self) -> List[Dict]:
        all_sources = []
        for data_source in data_source_collection.find(projection={"name"}):
            data_source["id"] = data_source.pop("_id")
            all_sources.append({"id": data_source["id"], "name": data_source["name"]})

        return all_sources

    def create(self, id: str, document: DataSourceRequest):
        document = document.dict()
        document["_id"] = id
        try:
            self.validate_data_source(document)
            result = data_source_collection.insert_one(document)
        except InvalidEntityException:
            raise InvalidEntityException(f"Failed to create data source '{id}'. The posted entity is invalid...")
        except DuplicateKeyError:
            logger.warning(f"Tried to create a datasource that already exists ('{id}')")
            raise DataSourceAlreadyExistsException(id)
        return str(result.inserted_id)

    def get(self, id: str) -> DataSource:
        data_source = data_source_collection.find_one(filter={"_id": id})
        if not data_source:
            raise DataSourceNotFoundException(id)
        return DataSource.from_dict(data_source)


def get_data_source(data_source_id: str) -> DataSource:
    return DataSourceRepository().get(data_source_id)
