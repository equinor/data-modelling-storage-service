import re
from functools import lru_cache
from typing import List, Union

from api.classes.tree_node import Node
from api.core.storage.repository_exceptions import (
    EntityNotFoundException,
    RootPackageNotFoundException,
)
from api.core.storage.internal.data_source_repository import get_data_source
from api.utils.helper_functions import get_data_source_and_path, get_package_and_path
from api.utils.logging import logger

from api.classes.blueprint import Blueprint
from api.classes.dto import DTO
from api.config import Config
from api.services.database import dmt_database


def _find_document_in_package_by_path(package: DTO, path_elements: List[str], repository) -> Union[str, dict, None]:
    """
    :param package: A Package object to search down into
    :param path_elements: A list representation of the path to the document. Starting from _this_ package

    :return: The uid of the requested document, or the next Package object in the path.
    """
    if len(path_elements) == 1:
        target = path_elements[0]
        file = next((f for f in package["content"] if f.get("name") == target), None)
        if not file:
            logger.error(f"The document {target} could not be found in the package {package.name}")
            return
        return file["_id"]
    else:
        next_package = next((p for p in package["content"] if p["name"] == path_elements[0]), None)
        if not next_package:
            logger.error(f"The package {path_elements[0]} could not be found in the package {package.name}")
            return
        next_package: DTO = repository.first({"_id": next_package["_id"]})
        del path_elements[0]
        return _find_document_in_package_by_path(next_package, path_elements, repository)


def get_document_uid_by_path(path: str, repository) -> Union[str, None]:
    root_package_name, path_elements = get_package_and_path(path)
    root_package: DTO = repository.first({"name": root_package_name, "isRoot": True})
    if not root_package:
        raise RootPackageNotFoundException(repository.name, root_package_name)
    # Check if it's a root-package
    if not path_elements:
        return root_package.uid
    uid = _find_document_in_package_by_path(root_package, path_elements, repository)
    if not uid:
        raise EntityNotFoundException(path)
    return uid


def get_document_by_ref(type_ref) -> DTO:
    # TODO: Get DataSource from Package's config file
    data_source_id, path = get_data_source_and_path(type_ref)
    document_repository = get_data_source(data_source_id)
    type_id = get_document_uid_by_path(path, document_repository)
    if not type_id:
        raise EntityNotFoundException(uid=type_ref)
    return document_repository.get(uid=type_id)


def duplicate_filename(parent_node: Node, new_file_name: str):
    if next((child for child in parent_node.children if child.name == new_file_name), None):
        return True


def url_safe_name(name: str) -> bool:
    # Only allows alphanumeric, underscore, and dash
    expression = re.compile("^[A-Za-z0-9_-]*$")
    match = expression.match(name)
    if match:
        return True


def wipe_db():
    print("Dropping all collections")
    # FIXME: Read names from the database
    for name in [
        Config.BLUEPRINT_COLLECTION,
        Config.ENTITY_COLLECTION,
        Config.SYSTEM_COLLECTION,
        "documents",
        "fs.chunks",
        "fs.files",
    ]:
        print(f"Dropping collection '{name}'")
        dmt_database.drop_collection(name)


@lru_cache(maxsize=Config.CACHE_MAX_SIZE)
def get_blueprint_cached(type: str) -> Blueprint:
    try:
        document: DTO = get_document_by_ref(type)
        return Blueprint(document)
    except Exception as error:
        logger.exception(error)
        raise EntityNotFoundException(uid=type)


class BlueprintProvider:
    def __init__(self):
        self.get_blueprint = get_blueprint_cached

    def get_blueprint(self, type: str) -> Blueprint:
        try:
            logger.debug(f"Fetching Blueprint {type}")
            document = self.get_blueprint(type)
            return document
        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(uid=type)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)
