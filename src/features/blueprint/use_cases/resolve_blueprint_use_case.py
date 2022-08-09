from typing import List

from authentication.models import User

from enums import SIMOS

from storage.internal.data_source_repository import get_data_source
from common.exceptions import EntityNotFoundException
from common.utils.string_helpers import split_absolute_ref


def find_package_with_document(data_source: str, document_id: str, user) -> dict:
    repository = get_data_source(data_source, user)
    packages: List[dict] = repository.find(
        {"type": SIMOS.PACKAGE.value, "content": {"$elemMatch": {"_id": document_id}}}
    )
    if not packages:
        raise EntityNotFoundException(document_id, "Failed to find package")
    return packages[0].data


def resolve_blueprint_use_case(user: User, absolute_id: str):
    data_source, document_id, attr = split_absolute_ref(absolute_id)
    root_package_found = False
    path_elements = []
    package = find_package_with_document(data_source, document_id, user)
    blueprint_name = next((c["name"] for c in package["content"] if c["_id"] == document_id))
    path_elements.append(blueprint_name)
    path_elements.append(package["name"])
    next_document_id = package["_id"]
    while not root_package_found:
        package = find_package_with_document(data_source, next_document_id, user)
        path_elements.append(package["name"])
        root_package_found = package["isRoot"]
        next_document_id = package["_id"]
    path_elements.reverse()
    return data_source + "/" + "/".join(path_elements)
