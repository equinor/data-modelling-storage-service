from typing import List, Union

from authentication.models import User
from common.exceptions import (
    ApplicationException,
    BadRequestException,
    NotFoundException,
)
from common.utils.string_helpers import split_dmss_ref
from domain_classes.repository import Repository
from storage.internal.data_source_repository import get_data_source


def get_root_package(root_package_name: str, repository: Repository) -> dict:
    root_package: [dict] = repository.find({"name": root_package_name, "isRoot": True})
    if not root_package:
        raise NotFoundException(
            f"No root package with name '{root_package_name}', in data source '{repository.name}' could be found."
        )
    if len(root_package) > 2:
        raise ApplicationException(
            f"More than 1 root package with name '{root_package_name}' "
            + "was returned from DataSource. That should not happen..."
        )
    return root_package[0]


def _get_document_uid_by_path(package: dict, path_elements: List[str], data_source: Repository) -> str:
    """
    :param package: A Package object to search down into
    :param path_elements: A list representation of the path to the document. Starting from _this_ package

    :return: The uid of the requested document, or the next Package object in the path.
    """
    if len(path_elements) == 1:
        target = path_elements[0]
        file = next((f for f in package["content"] if f.get("name") == target), None)
        if not file:
            raise NotFoundException(f"The document {target} could not be found in the package {package['name']}")
        return file["_id"]

    next_package_ref = next((p for p in package["content"] if p["name"] == path_elements[0]), None)
    if not next_package_ref:
        raise NotFoundException(f"The package {path_elements[0]} could not be found in the package {package['name']}")
    next_package: dict = data_source.get(next_package_ref["_id"])
    if not next_package:
        raise NotFoundException(
            f"Could not find a package '{next_package_ref['_id']}' in datasource {data_source.name}"
        )
    del path_elements[0]
    return _get_document_uid_by_path(next_package, path_elements, data_source)


def get_document_uid_by_path(dotted_path: str, repository: Repository) -> Union[str, None]:
    path_elements = dotted_path.split("/")
    root_package_name = path_elements.pop(0)
    root_package = get_root_package(root_package_name, repository)
    # Check if it's a root-package
    if not path_elements:
        return root_package["_id"]
    uid = _get_document_uid_by_path(root_package, path_elements, repository)
    return uid


def get_document_by_absolute_path(absolute_path: str, user: User) -> dict:
    """Fetches the document from any supported protocol by the absolute path which must be on the format
    PROTOCOL://ADDRESS"""

    try:
        protocol, address = absolute_path.split("://", 1)
    except ValueError:
        raise BadRequestException(f"Invalid format. The value '{absolute_path}' does not specify a protocol.")
    match protocol:
        case "dmss":  # The entity should be fetched from a DataSource in this DMSS instance
            data_source_id, path, attribute = split_dmss_ref(address)
            document_repository = get_data_source(data_source_id, user)
            type_id = get_document_uid_by_path(path, document_repository)
            if not type_id:
                raise NotFoundException(message=f"Entity referenced with '{address}' could not be found")
            return document_repository.get(uid=type_id)
        case "http":  # The entity should be fetched by an HTTP call
            raise NotImplementedError
        case _:
            raise NotImplementedError
