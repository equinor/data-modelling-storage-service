from typing import Callable

from common.address import Address
from common.entity.is_reference import is_reference
from common.exceptions import ApplicationException
from common.providers.address_resolver import ResolvedAddress, resolve_address
from storage.data_source_class import DataSource


def resolve_reference_list(
    values: list, document_repository: DataSource, get_data_source, current_id, depth: int = 1, depth_count: int = 0
) -> list:
    if not values:  # Return an empty list
        return values

    value_sample = values[0]

    if isinstance(value_sample, list):  # Call recursively for nested lists
        return [
            resolve_reference_list(value, document_repository, get_data_source, current_id, depth, depth_count)
            for value in values
        ]

    if is_reference(value_sample):
        return [
            get_complete_sys_document(value, document_repository, get_data_source, current_id, depth, depth_count)
            for value in values
        ]

    if isinstance(value_sample, dict):
        return [
            resolve_references_in_entity(value, document_repository, get_data_source, current_id, depth, depth_count)
            for value in values
        ]

    # Values are primitive, return as is.
    return values


def get_complete_sys_document(
    reference: dict,
    data_source: DataSource,
    get_data_source,
    current_id: str = None,
    depth: int = 1,
    depth_count: int = 0,
) -> dict | list:
    if not reference["address"]:
        raise ApplicationException("Invalid link. Missing 'address'", data=reference)
    address = Address.from_relative(reference["address"], current_id, data_source.name)

    resolved_address: ResolvedAddress = resolve_address(address, get_data_source)
    if is_reference(resolved_address.entity):
        resolved_address = resolve_address(
            Address.from_relative(
                resolved_address.entity["address"], resolved_address.document_id, resolved_address.data_source_id
            ),
            get_data_source,
        )

    # For supporting ^ references, update the current document id
    if "_id" in resolved_address.entity:
        current_id = resolved_address.entity["_id"]

    return resolve_references_in_entity(
        resolved_address.entity, data_source, get_data_source, current_id, depth, depth_count
    )


def resolve_references_in_entity(
    entity: dict,
    data_source: DataSource,
    get_data_source: Callable,
    current_id: str | None,
    depth: int,
    depth_count: int,
) -> dict:
    """
    Resolve references inside an entity.

    Resolving a reference means that a link or storage reference object (of type Reference) is substituted by the full document it refers to (defined in the address part of the reference object).
    The depth parameter determines how far down into the document we want to resolve references.
    """
    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return entity

    for key, value in entity.items():
        if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
            if not value:
                continue
            if isinstance(value, list):  # If it's a list, resolve any references
                entity[key] = resolve_reference_list(
                    value, data_source, get_data_source, current_id, depth, depth_count + 1
                )
            else:
                if is_reference(value):
                    if depth_count <= depth:
                        entity[key] = get_complete_sys_document(
                            value, data_source, get_data_source, current_id, depth, depth_count + 1
                        )
                        continue
                    entity[key] = value
                else:
                    entity[key] = resolve_references_in_entity(
                        value, data_source, get_data_source, current_id, depth, depth_count + 1
                    )

    return entity
