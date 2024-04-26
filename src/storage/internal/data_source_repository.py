import json

from pydantic import BaseModel
from pymongo.errors import ServerSelectionTimeoutError

from authentication.access_control import assert_user_has_access
from authentication.models import AccessControlList, AccessLevel, User
from common.exceptions import (
    ApplicationException,
    BadRequestException,
    NotFoundException,
)
from common.utils.logging import logger
from restful.request_types.create_data_source import DataSourceRequest
from services.database import data_source_db
from storage.data_source_class import DataSource

RESERVED_MONGO_DATABASES = ("admin", "local", "config", "dmss-internal")


class DataSourceInformation(BaseModel):
    id: str
    name: str
    host: str | None = None
    type: str | None = None


class DataSourceRepository:
    def __init__(self, user: User, get_blueprint=None):
        self.user = user
        self.get_blueprint = get_blueprint

    @staticmethod
    def validate_data_source(document: dict):
        for repo in document["repositories"].values():
            if repo.get("name"):
                raise BadRequestException("A repository specification may not have the 'name' key.")
            if repo["type"] == "mongo-db":
                if repo["database"] in RESERVED_MONGO_DATABASES:
                    raise BadRequestException(
                        f"The database named '{repo['database']}' " "is a system reserved database name."
                    )

    @staticmethod
    def validate_repository(repo: dict):
        try:
            if repo.get("name"):
                raise BadRequestException("A repository specification may not have the 'name' key.")
            if repo["type"] == "mongo-db":
                if repo["database"] in RESERVED_MONGO_DATABASES:
                    raise BadRequestException(
                        f"The database named '{repo['database']}' " "is a system reserved database name."
                    )
        except Exception as ex:
            raise BadRequestException(ex) from ex

    def list(self) -> list[dict]:
        all_sources = []
        for data_source_id in data_source_db.list_keys():
            all_sources.append({"id": data_source_id, "name": data_source_id})

        all_sources.sort(key=lambda x: x["name"])
        return all_sources

    def create(self, id: str, document: DataSourceRequest):
        assert_user_has_access(AccessControlList.default(), AccessLevel.WRITE, self.user)
        if data_source_db.get(id):
            logger.warning(f"Tried to create a datasource that already exists ('{id}')")
            raise BadRequestException(f"Tried to create a datasource that already exists ('{id}')")
        document = document.dict()
        document["_id"] = id
        self.validate_data_source(document)
        data_source_db.set(id, document)

        return id

    def get(self, id: str) -> DataSource:
        try:
            data_source = data_source_db.get(id)
        except ServerSelectionTimeoutError as ex:
            logger.error("Failed to establish connection to internal database")
            raise ApplicationException(debug="Internal storage error") from ex
        if not data_source:
            raise NotFoundException(
                message=f"The data source, with id '{id}' could not be found",
                debug=f"No data source with id '{id}' could be found in the internal DS repository",
            )
        return DataSource.from_dict(data_source, user=self.user, get_blueprint=self.get_blueprint)

    def update_access_control(self, data_source_id: str, acl: AccessControlList) -> None:
        data_source: DataSource = self.get(data_source_id)
        assert_user_has_access(data_source.acl, AccessLevel.WRITE, self.user)
        data_source_dict = json.loads(data_source_db.get(data_source_id))
        data_source_dict["acl"] = acl.to_dict()
        data_source_db.set(data_source_id, data_source)


def get_data_source(data_source_id: str, user: User, get_blueprint) -> DataSource:
    return DataSourceRepository(user, get_blueprint).get(data_source_id)
