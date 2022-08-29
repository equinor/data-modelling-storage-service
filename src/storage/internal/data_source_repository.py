from typing import Dict, List

from pymongo.errors import DuplicateKeyError

from authentication.access_control import DEFAULT_ACL, access_control
from authentication.models import ACL, AccessLevel, User
from common.exceptions import BadRequestException, NotFoundException
from common.utils.logging import logger
from enums import RepositoryType
from restful.request_types.create_data_source import DataSourceRequest
from services.database import data_source_collection
from storage.data_source_class import DataSource

RESERVED_MONGO_DATABASES = ("admin", "local", "config", "dmss-internal")


class DataSourceRepository:
    def __init__(self, user: User):
        self.user = user

    @staticmethod
    def validate_data_source(document: dict):
        try:
            for repo in document["repositories"].values():
                if repo.get("name"):
                    raise BadRequestException("A repository specification may not have the 'name' key.")
                if repo["type"] == RepositoryType.MONGO.value:
                    if repo["database"] in RESERVED_MONGO_DATABASES:
                        raise BadRequestException(
                            f"The database named '{repo['database']}' " "is a system reserved database name."
                        )
        except KeyError as e:
            raise KeyError(e)
        except Exception as error:
            raise BadRequestException(error)

    @staticmethod
    def validate_repository(repo: dict):
        try:
            if repo.get("name"):
                raise BadRequestException("A repository specification may not have the 'name' key.")
            if repo["type"] == RepositoryType.MONGO.value:
                if repo["database"] in RESERVED_MONGO_DATABASES:
                    raise BadRequestException(
                        f"The database named '{repo['database']}' " "is a system reserved database name."
                    )
        except KeyError as e:
            raise KeyError(e)
        except Exception as error:
            raise BadRequestException(error)

    def list(self) -> List[Dict]:
        all_sources = []
        for data_source in data_source_collection.find(projection={"name"}):
            data_source["id"] = data_source.pop("_id")
            all_sources.append({"id": data_source["id"], "name": data_source["name"]})

        return all_sources

    def create(self, id: str, document: DataSourceRequest):
        access_control(DEFAULT_ACL, AccessLevel.WRITE, self.user)
        document = document.dict()
        document["_id"] = id
        try:
            self.validate_data_source(document)
            result = data_source_collection.replace_one({"_id": id}, document, upsert=True)
        except BadRequestException:
            raise BadRequestException(
                message=f"Failed to create data source '{id}'. The posted entity is invalid...", data=document
            )
        except DuplicateKeyError:
            logger.warning(f"Tried to create a datasource that already exists ('{id}')")
            raise BadRequestException(f"Tried to create a datasource that already exists ('{id}')")
        return str(result.upserted_id)

    def get(self, id: str) -> DataSource:
        data_source = data_source_collection.find_one(filter={"_id": id})
        if not data_source:
            raise NotFoundException(
                message=f"The data source, with id '{id}' could not be found",
                debug=f"No data source with id '{id}' could be found in the internal DS repository",
            )
        return DataSource.from_dict(data_source, user=self.user)

    def update_access_control(self, data_source_id: str, acl: ACL) -> None:
        data_source: DataSource = self.get(data_source_id)
        access_control(data_source.acl, AccessLevel.WRITE, self.user)
        data_source_collection.update_one(filter={"_id": data_source.name}, update={"$set": {"acl": acl.dict()}})


def get_data_source(data_source_id: str, user: User) -> DataSource:
    return DataSourceRepository(user).get(data_source_id)
