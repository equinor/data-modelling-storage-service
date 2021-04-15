from typing import List, Union

from domain_classes.dto import DTO
from storage.internal.data_source_repository import get_data_source
from utils.exceptions import EntityNotFoundException, RootPackageNotFoundException
from utils.logging import logger
from utils.string_helpers import get_data_source_and_path, get_package_and_path


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
