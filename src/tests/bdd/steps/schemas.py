import json

from behave import given

from config import config
from domain_classes.dto import DTO
from restful.request_types.create_data_source import DataSourceRequest
from storage.internal.data_source_repository import DataSourceRepository, get_data_source
from utils.logging import logger
from utils.package_import import import_package


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: DTO = DTO(uid=uid, data=json.loads(context.text))
    document_repository = get_data_source(data_source_id, context.user)
    document_repository.update(document)


@given("the system data source and SIMOS core package are available")
def step_impl(context):
    # Add system data source:
    document = {
        "_id": "system",
        "name": "system",
        "repositories": {
            "system": {
                "data_types": ["default"],
                "host": "db",
                "port": 27017,
                "username": "maf",
                "password": "maf",
                "tls": False,
                "database": "DMSS-core-bdd",
                "collection": "DMSS-core-bdd",
                "type": "mongo-db",
            }
        },
    }
    DataSourceRepository(context.user).create(document["name"], DataSourceRequest(**document))

    # Import SIMOS package
    logger.setLevel("ERROR")
    import_package(f"{config.APPLICATION_HOME}/system/SIMOS", context.user, is_root=True, data_source="system")
    logger.setLevel("INFO")
