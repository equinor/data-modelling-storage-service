from typing import Callable

from common.address import Address
from common.exceptions import ApplicationException
from common.utils.is_reference import is_link, is_reference
from common.utils.resolve_reference import ResolvedReference, resolve_address
from storage.data_source_class import DataSource


def resolve_reference_list(
    values: list,
    document_repository: DataSource,
    get_data_source,
    current_id,
    depth: int = 1,
    depth_count: int = 0,
    resolve_links: bool = False,
) -> list:
    if not values:  # Return an empty list
        return values

    value_sample = values[0]

    if isinstance(value_sample, list):  # Call recursively for nested lists
        return [
            resolve_reference_list(
                value, document_repository, get_data_source, current_id, depth, depth_count, resolve_links
            )
            for value in values
        ]

    if is_reference(value_sample):
        if resolve_links or not is_link(value_sample):
            return [
                get_complete_sys_document(
                    value, document_repository, get_data_source, current_id, depth, depth_count, resolve_links
                )
                for value in values
            ]
        return values  # If we're not resolving references, return them as is

    if isinstance(value_sample, dict):
        return [
            resolve_references_in_entity(
                value, document_repository, get_data_source, current_id, depth, depth_count, resolve_links
            )
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
    resolve_links: bool = False,
) -> dict | list:
    if not reference["address"]:
        raise ApplicationException("Invalid link. Missing 'address'", data=reference)
    address = Address.from_relative(reference["address"], current_id, data_source.name)

    resolved_reference: ResolvedReference = resolve_address(address, get_data_source)
    if is_reference(resolved_reference.entity) and resolve_links:
        resolved_reference = resolve_address(
            Address.from_relative(
                resolved_reference.entity["address"], resolved_reference.document_id, resolved_reference.data_source_id
            ),
            get_data_source,
        )

    # Only update if the resolved reference has id (since it can point to a document that are contained in another document)
    if is_link(reference) and "_id" in resolved_reference.entity:
        # For supporting ^ references, update the current document id
        current_id = resolved_reference.entity["_id"]

    return resolve_references_in_entity(
        resolved_reference.entity, data_source, get_data_source, current_id, depth, depth_count, resolve_links
    )


def resolve_references_in_entity(
    entity: dict,
    data_source: DataSource,
    get_data_source: Callable,
    current_id: str | None,
    depth: int = 1,
    depth_count: int = 0,
    resolve_links: bool = False,
) -> dict:
    """
    Resolve references inside an entity.

    Resolving a reference means that a link or storage reference object (of type Reference) is substituted by the full document it refers to (defined in the address part of the reference object).
    The depth parameter determines how far down into the document we want to resolve references.
    The resolve_links parameter determines whether or not to resolve reference objects with referenceType equal to 'link'
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
                    value, data_source, get_data_source, current_id, depth, depth_count + 1, resolve_links
                )
            else:
                if is_reference(value):
                    # Only resolve links if 'resolve_links' are passed.
                    # Always resolve "storage" references
                    if resolve_links or not is_link(value):
                        entity[key] = get_complete_sys_document(
                            value, data_source, get_data_source, current_id, depth, depth_count + 1, resolve_links
                        )
                        continue
                    entity[key] = value
                else:
                    entity[key] = resolve_references_in_entity(
                        value, data_source, get_data_source, current_id, depth, depth_count + 1, resolve_links
                    )

    return entity
