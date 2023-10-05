import re
from typing import List

from authentication.models import User
from common.address import Address
from common.exceptions import ApplicationException, NotFoundException
from common.providers.address_resolver import resolve_address
from enums import SIMOS
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source


def find_package_with_document(data_source: str, document_id: str, user) -> dict:
    repository = get_data_source(data_source, user)
    packages: List[dict] = repository.find(
        {"type": SIMOS.PACKAGE.value, "content": {"$elemMatch": {"address": document_id}}}
    )
    if not packages:
        raise NotFoundException(document_id, "Failed to find package")
    return packages[0]


def resolve_references(values: list, data_source_id: str, user: User) -> list:
    data_source: DataSource = get_data_source(data_source_id, user)
    return [
        resolve_address(
            Address.from_relative(value["address"], None, data_source.name),
            lambda data_source_name: get_data_source(data_source_name, user),
        ).entity
        for value in values
    ]


def resolve_blueprint_use_case(user: User, address: str):
    address_obj = Address.from_absolute(address)
    path_elements = []
    if not address_obj.path or not re.search(r"^\$[a-z0-9]+$", address_obj.path):
        raise ApplicationException(f"Incorrect address {address}. Address should point directly to an id")
    package = find_package_with_document(address_obj.data_source, address_obj.path, user)
    root_package_found = package["isRoot"]
    blueprint_name = next(
        (
            c["name"]
            for c in resolve_references(package["content"], address_obj.data_source, user)
            if f"${c['_id']}" == address_obj.path
        )
    )
    path_elements.append(blueprint_name)
    path_elements.append(package["name"])
    next_document_id = f"${package['_id']}"
    while not root_package_found:
        package = find_package_with_document(address_obj.data_source, next_document_id, user)
        path_elements.append(package["name"])
        root_package_found = package["isRoot"]
        next_document_id = f"${package['_id']}"
    path_elements.reverse()
    return f"{address_obj.protocol}://{address_obj.data_source}/{'/'.join(path_elements)}"
