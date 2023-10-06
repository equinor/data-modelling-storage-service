import re
from dataclasses import dataclass
from typing import Any, Callable, Tuple, Union

from common.address import Address
from common.entity.find import find
from common.entity.has_key_value_pairs import has_key_value_pairs
from common.entity.is_reference import is_reference
from common.exceptions import ApplicationException, NotFoundException
from enums import REFERENCE_TYPES, SIMOS
from storage.data_source_class import DataSource


def _next_path_part(path: str) -> Tuple[str, Union[str, None], str]:
    """Utility to get next path part."""
    content = path  # Default to path
    deliminator = None
    remaining_path = ""

    search = re.search(r"[.|/|\]|\[]", path)  # Search for next deliminator
    if search:
        deliminator = search.group(0)
        # Extract the content (the text between the two deliminators)
        content = path[: search.end() - 1]
        # Remove the extracted content (including deliminator), so that we don't handle it again.
        remaining_path = path[search.end() :]
    return content, deliminator, remaining_path


@dataclass
class IdItem:
    """Points to an id."""

    id: str

    def get_entry_point(self, data_source: DataSource) -> Tuple[dict, str]:
        if data_source.get_lookup(self.id).storage_affinity == "blob":
            # Do not resolve any binary data, just return a reference to it.
            # Getting the binary data needs to be handled by the consumer (e.g frontend).
            return {
                "type": SIMOS.REFERENCE.value,
                "address": f"${self.id}",
                "referenceType": REFERENCE_TYPES.STORAGE.value,
            }, self.id
        # Get the document from the data source
        result = data_source.get(self.id)
        if not result:
            raise NotFoundException(
                f"No document with id '{self.id}' could be found in data source '{data_source.name}'."
            )
        return result, self.id

    def __repr__(self):
        return f"${self.id}"


@dataclass
class QueryItem:
    """Query a list for a document."""

    def __repr__(self):
        return f'Query="{self.query_as_str}"'

    def __init__(self, query: str):
        self.query_as_str = query

        self.query_as_dict: dict[str, Any] = {}
        for pair in self.query_as_str.split(","):
            key, value = pair.split("=")
            if value == "True" or value == "False":
                self.query_as_dict[key] = bool(value)
            else:
                self.query_as_dict[key] = value

    def get_entry_point(self, data_source: DataSource) -> Tuple[dict, str]:
        result: list[dict] = data_source.find(self.query_as_dict)
        if not result:
            raise NotFoundException(
                f"No document that match '{self.query_as_str}' could be found in data source '{data_source.name}'."
            )
        if len(result) > 2:
            raise ApplicationException(
                f"More than 1 document that match '{self.query_as_str}' was returned from DataSource. That should not happen..."
            )
        return result[0], result[0]["_id"]

    def get_child(
        self, entity: dict | list, document_id: str, data_source: DataSource, get_data_source: Callable
    ) -> Tuple[Any, str]:
        if isinstance(entity, dict) and is_reference(entity):
            resolved_ref = resolve_address(
                Address.from_relative(entity["address"], document_id, data_source.name), get_data_source
            )
            entity = resolved_ref.entity
            document_id = resolved_ref.document_id

        # Search inside an existing document (need to resolve any references first before trying to compare against filter)
        elements = [
            resolve_address(Address.from_relative(f["address"], document_id, data_source.name), get_data_source).entity
            if is_reference(f)
            else f
            for f in entity
        ]  # Resolve any references
        for index, element in enumerate(elements):
            if isinstance(element, dict) and has_key_value_pairs(element, self.query_as_dict):
                return entity[index], f"[{index}]"
        raise NotFoundException(f"No object matches filter '{self.query_as_str}'", data={"elements": elements})


@dataclass
class AttributeItem:
    """Move into a key of an object or find an item in a list based on index position."""

    path: str

    def __repr__(self):
        return f'Attribute="{self.path}"'

    def get_child(
        self, entity: dict | list, document_id: str, data_source: DataSource, get_data_source: Callable
    ) -> tuple[Any, str]:
        if isinstance(entity, dict) and is_reference(entity):
            entity = resolve_address(
                Address.from_relative(entity["address"], document_id, data_source.name), get_data_source
            ).entity
        try:
            result = find(entity, [self.path])
        except (IndexError, ValueError, KeyError):
            if isinstance(entity, dict):
                raise NotFoundException(
                    f"Invalid attribute '{self.path}'. Valid attributes are '{list(entity.keys())}'."
                )
            else:
                raise NotFoundException(f"Invalid index '{self.path}'. Valid indices are < {len(entity)}.")

        return result, self.path


def path_to_path_items(path: str) -> list[AttributeItem | QueryItem | IdItem]:
    """Split up the path into path items.
    The path used as input to this function should not include protocol or data source.
    """
    queries = re.findall(r"\(([^\)]+)\)", path)
    if queries:
        # Split the path into the pieces surrounding the queries and remove trailing [( and )]
        remaining_ref_parts = re.split("|".join([re.escape(q) for q in queries]), path)
        remaining_ref_parts = list(map(lambda x: re.sub(r"\[?\($|^\)\]?", "", x), remaining_ref_parts))

        items = _path_to_path_items(remaining_ref_parts[0], [], None)
        for index, query in enumerate(queries):
            items.append(QueryItem(query=query))
            items = _path_to_path_items(remaining_ref_parts[index + 1], [*items], None)
        return items
    else:
        return _path_to_path_items(path, [], None)


def _path_to_path_items(path: str, items, prev_deliminator) -> list[AttributeItem | QueryItem | IdItem]:
    if len(path) == 0:
        return items

    content, deliminator, remaining_path = _next_path_part(path)
    if content == "":
        # If the original path starts with a deliminator (e.g. /)
        # then there is no content.
        # The deliminator is extracted from the remaining path.
        # Continue resolve the remaining path.
        return _path_to_path_items(remaining_path, items, deliminator)

    if "$" in content:  # By id
        items.append(IdItem(content[1:]))
    elif len(items) == 0:  # By root package
        items.append(QueryItem(query=f"name={content},isRoot=True"))
    elif prev_deliminator == "/":  # By package
        items.append(AttributeItem("content"))
        items.append(QueryItem(query=f"name={content}"))
    elif prev_deliminator == "[" and deliminator == "]":  # By list index
        items.append(AttributeItem(f"[{content}]"))
    elif prev_deliminator == ".":  # By attribute
        items.append(AttributeItem(content))
    else:
        raise Exception(f"Not supported path format: {path}")

    return _path_to_path_items(remaining_path, items, deliminator)


def resolve_path_items(
    data_source: DataSource,
    path_items: list[AttributeItem | QueryItem | IdItem],
    get_data_source: Callable,
) -> tuple[list | dict, list[str]]:
    if len(path_items) == 0 or isinstance(path_items[0], AttributeItem):
        raise NotFoundException(f"Invalid path_items {path_items}.")
    entity, id = path_items[0].get_entry_point(data_source)
    path = [id]
    for index, ref_item in enumerate(path_items[1:]):
        if isinstance(ref_item, IdItem):
            raise NotFoundException(f"Invalid path_items {path_items}.")
        entity, attribute = ref_item.get_child(entity, path[0], data_source, get_data_source)
        if is_reference(entity) and index < len(path_items) - 2:
            # Found a new document, use that as new starting point for the attribute path
            address = Address.from_relative(entity["address"], path[0], data_source.name)
            resolved_reference = resolve_address(address, get_data_source)
            path = [resolved_reference.document_id, *resolved_reference.attribute_path]
        else:
            path.append(attribute)
        if not isinstance(entity, (list, dict)):
            raise NotFoundException(f"Path {path} leads to a primitive value.")
    return entity, path


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
    document, path = resolve_path_items(data_source, path_items, get_data_source)
    return ResolvedAddress(
        entity=document,
        data_source_id=address.data_source,
        document_id=str(path[0]),
        attribute_path=path[1:],
    )
