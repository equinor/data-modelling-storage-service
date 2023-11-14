from collections.abc import Callable
from dataclasses import dataclass

from common.address import Address
from common.entity.is_reference import is_reference
from common.exceptions import ApplicationException, NotFoundException
from common.providers.address_resolver.path_items import (
    AttributeItem,
    IdItem,
    QueryItem,
)
from common.providers.address_resolver.path_to_path_items import path_to_path_items
from storage.data_source_class import DataSource


def _resolve_path_items(
    data_source: DataSource,
    path_items: list[AttributeItem | QueryItem | IdItem],
    get_data_source: Callable,
) -> tuple[list | dict, list[str], str]:
    if len(path_items) == 0 or isinstance(path_items[0], AttributeItem):
        raise NotFoundException(f"Invalid path_items {path_items}.")
    entity, id = path_items[0].get_entry_point(data_source)
    path = [id]
    data_source_name = data_source.name
    for index, ref_item in enumerate(path_items[1:]):
        if isinstance(ref_item, IdItem):
            raise NotFoundException(f"Invalid path_items {path_items}.")
        entity, attribute = ref_item.get_child(
            entity, path[0], data_source, get_data_source, resolve_address=resolve_address
        )
        if is_reference(entity) and index < len(path_items) - 2:
            # Found a new document, use that as new starting point for the attribute path
            address = Address.from_relative(entity["address"], path[0], data_source.name)
            resolved_reference = resolve_address(address, get_data_source)
            path = [resolved_reference.document_id, *resolved_reference.attribute_path]
            data_source_name = resolved_reference.data_source_id
        else:
            path.append(attribute)
        if not isinstance(entity, list | dict):
            raise NotFoundException(f"Path {path} leads to a primitive value.")
    return entity, path, data_source_name


@dataclass(frozen=True)
class ResolvedAddress:
    data_source_id: str
    document_id: str
    attribute_path: list[str]
    entity: dict | list


def resolve_address(address: Address, get_data_source: Callable) -> ResolvedAddress:
    """Resolve the address into a document.

    We extract data_source, document_id, attribute_path from the address and also find the document the
    address refers to. The information is collected into a ResolvedReference object and returned.
    """
    if not address.path:
        raise ApplicationException(f"Failed to resolve reference. Got empty address path from {address}")

    path_items = path_to_path_items(address.path)

    # The first reference item should always be a DataSourceItem
    data_source = get_data_source(address.data_source)
    document, path, data_source = _resolve_path_items(data_source, path_items, get_data_source)

    return ResolvedAddress(
        entity=document,
        data_source_id=data_source,
        document_id=str(path[0]),
        attribute_path=path[1:],
    )
