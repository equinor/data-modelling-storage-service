from pydantic import conint

from authentication.models import User
from common.address import Address
from common.exceptions import BadRequestException
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_nested_dict_attribute(entity: dict | list, path_list: list[str]) -> dict | list:
    try:
        if isinstance(entity, list):
            path_list[0] = int(path_list[0].strip("[]"))  # type: ignore
        if len(path_list) == 1:
            return entity[path_list[0]]  # type: ignore
        return get_nested_dict_attribute(entity[path_list[0]], path_list[1:])  # type: ignore
    except (KeyError, IndexError) as e:
        raise BadRequestException(f"Attribute/Item '{path_list[0]}' does not exists in '{entity}'") from e


def get_document_use_case(
    user: User,
    address: str,
    depth: conint(gt=-1, lt=1000),  # type: ignore
    repository_provider=get_data_source,
):
    """Get document by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    address_object = Address.from_absolute(address)
    resolved_document, resolved_address = document_service.resolve_document(address_object, depth)
    if len(resolved_address.attribute_path) > 0:
        return get_nested_dict_attribute(resolved_document, resolved_address.attribute_path)
    return resolved_document
