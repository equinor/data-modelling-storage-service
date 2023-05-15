import json

from behave import given

from authentication.models import User
from common.utils.logging import logger
from common.utils.package_import import import_package
from config import config
from features.lookup_table.use_cases.create_lookup_table import (
    create_lookup_table_use_case,
)
from restful.request_types.create_data_source import DataSourceRequest
from storage.internal.data_source_repository import (
    DataSourceRepository,
    get_data_source,
)


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: dict = json.loads(context.text)
    document["_id"] = uid
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
    logger_level_before = logger.level
    logger.setLevel("ERROR")
    import_package(f"{config.APPLICATION_HOME}/system/SIMOS", context.user, is_root=True, data_source_name="system")
    logger.setLevel(logger_level_before)

    user = User(user_id=config.DMSS_ADMIN)
    create_lookup_table_use_case(["system/SIMOS/recipe_links"], "DMSS", user)
