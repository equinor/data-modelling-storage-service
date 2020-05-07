import json

from behave import given, when, then

from api.core.repository import Repository
from api.core.repository.repository_factory import get_repository
from api.utils.logging import logger
from api.utils.package_import import import_package

from api.classes.dto import DTO
from api.config import Config


@given("data modelling tool templates are imported")
def step_impl(context):
    for folder in Config.SYSTEM_FOLDERS:
        logger.setLevel("ERROR")
        import_package(f"{Config.APPLICATION_HOME}/core/{folder}", collection=Config.SYSTEM_COLLECTION, is_root=True)
        logger.setLevel("INFO")


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: DTO = DTO(uid=uid, data=json.loads(context.text))
    document_repository: Repository = get_repository(data_source_id)
    document_repository.add(document)
