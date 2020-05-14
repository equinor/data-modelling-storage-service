import json

from behave import given


from api.core.storage.internal.data_source_repository import get_data_source
from api.utils.logging import logger
from api.utils.package_import import import_package

from api.classes.dto import DTO
from api.config import Config


@given("data modelling tool templates are imported")
def step_impl(context):
    for folder in Config.SYSTEM_FOLDERS:
        logger.setLevel("ERROR")
        import_package(f"{Config.APPLICATION_HOME}/core/{folder}", is_root=True, data_source="system")
        logger.setLevel("INFO")


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: DTO = DTO(uid=uid, data=json.loads(context.text))
    document_repository = get_data_source(data_source_id)
    document_repository.add(document)
