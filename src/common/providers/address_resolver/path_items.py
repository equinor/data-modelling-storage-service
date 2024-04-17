from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from common.address import Address
from common.entity.find import find
from common.entity.has_key_value_pairs import has_key_value_pairs
from common.entity.is_reference import is_reference
from common.exceptions import ApplicationException, NotFoundException
from enums import REFERENCE_TYPES, SIMOS
from storage.data_source_interface import DataSource


@dataclass
class IdItem:
    """Points to an id."""

    id: str

    def get_entry_point(self, data_source: DataSource) -> tuple[dict, str]:
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

    def get_entry_point(self, data_source: DataSource) -> tuple[dict, str]:
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
        self,
        entity: dict | list,
        document_id: str,
        data_source: DataSource,
        get_data_source: Callable,
        resolve_address: Callable,
    ) -> tuple[Any, str]:
        if isinstance(entity, dict) and is_reference(entity):
            resolved_ref = resolve_address(
                Address.from_relative(entity["address"], document_id, data_source.name),
                get_data_source,
            )
            entity = resolved_ref.entity
            document_id = resolved_ref.document_id

        # Search inside an existing document (need to resolve any references first before trying to compare against filter)
        for index, f in enumerate(entity):
            resolved_entity = (
                resolve_address(
                    Address.from_relative(f["address"], document_id, data_source.name),
                    get_data_source,
                ).entity
                if is_reference(f)
                else f
            )
            if isinstance(resolved_entity, dict) and has_key_value_pairs(resolved_entity, self.query_as_dict):
                return entity[index], f"[{index}]"

        raise NotFoundException(f"No object matches filter '{self.query_as_str}'", data={"entity": entity})


@dataclass
class AttributeItem:
    """Move into a key of an object or find an item in a list based on index position."""

    path: str

    def __repr__(self):
        return f'Attribute="{self.path}"'

    def get_child(
        self,
        entity: dict | list,
        document_id: str,
        data_source: DataSource,
        get_data_source: Callable,
        resolve_address: Callable,
    ) -> tuple[Any, str]:
        if isinstance(entity, dict) and is_reference(entity):
            entity = resolve_address(
                Address.from_relative(entity["address"], document_id, data_source.name),
                get_data_source,
            ).entity
        try:
            result = find(entity, [self.path])
        except (IndexError, ValueError, KeyError) as ex:
            if isinstance(entity, dict):
                raise NotFoundException(
                    f"Invalid attribute '{self.path}'. Valid attributes are '{list(entity.keys())}'."
                ) from ex
            else:
                try:
                    int(self.path)
                    raise NotFoundException(
                        "'myList.0' is an invalid syntax for accessing items in a list. Use 'myList[0]' instead"
                    ) from ex
                except ValueError:
                    pass
                raise NotFoundException(f"Invalid index '{self.path}'. Valid indices are < {len(entity)}.") from ex

        return result, self.path
