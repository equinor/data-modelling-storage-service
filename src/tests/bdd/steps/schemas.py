import json

from behave import given

from config import Config
from domain_classes.dto import DTO
from services.database import dmt_database
from storage.internal.data_source_repository import get_data_source
from utils.logging import logger
from utils.package_import import import_package


@given("SIMOS core package are imported")
def step_impl(context):
    for folder in Config.SYSTEM_FOLDERS:
        logger.setLevel("ERROR")
        import_package(f"{Config.APPLICATION_HOME}/system/{folder}", is_root=True, data_source="system")
        logger.setLevel("INFO")


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: DTO = DTO(uid=uid, data=json.loads(context.text))
    document_repository = get_data_source(data_source_id)
    document_repository.add(document)


@given("the system data source and SIMOS core package are available")
def step_impl(context):
    # Add system data source:
    document = {
        "_id": "system",
        "name": "system",
        "repositories": {
            "system": {
                "dataTypes": ["default"],
                "host": "db",
                "port": 27017,
                "username": "maf",
                "password": "maf",
                "tls": False,
                "name": "system",
                "database": "local",
                "collection": "system",
                "type": "mongo-db",
            }
        },
    }
    dmt_database["data_sources"].insert_one(document)
    dmt_database.drop_collection("system")

    # Import SIMOS package
    logger.setLevel("ERROR")
    import_package(f"{Config.APPLICATION_HOME}/system/SIMOS", is_root=True, data_source="system")
    logger.setLevel("INFO")
