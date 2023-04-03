from common.exceptions import ApplicationException
from common.utils.is_reference import is_reference
from common.utils.resolve_reference import resolve_reference
from enums import SIMOS
from storage.data_source_class import DataSource


def resolve_reference_list(
    values: list, document_repository: DataSource, get_data_source, current_id, depth: int = 999, depth_count: int = 0
) -> list:
    if not values:  # Return an empty list
        return values
    resolved: list[dict | list] = []

    if isinstance(values[0], list):  # Call recursively for nested lists
        resolved = [
            resolve_reference_list(value, document_repository, get_data_source, current_id) for value in values
        ]
    for value in values:
        if is_reference(value):
            resolved.append(
                get_complete_sys_document(value, document_repository, get_data_source, current_id, depth, depth_count)
            )
        elif isinstance(value, dict):
            resolved.append(
                resolve_contained_dict(value, document_repository, get_data_source, current_id, depth, depth_count)
            )
        else:
            resolved.append(value)
    return resolved


def get_complete_sys_document(
    link_or_storage_address: dict,
    data_source: DataSource,
    get_data_source,
    current_id: str = None,
    depth: int = 999,
    depth_count: int = 0,
) -> dict:
    address = link_or_storage_address["ref"]

    if address.startswith("^"):
        # Replace ^ with an id reference that contains the current document id
        if not current_id:
            raise ApplicationException(
                "Current id is missing and therefore it is not possible to replace ^ with an id reference."
            )
        address = address.replace("^", f"${current_id}")

    document = resolve_reference(address, data_source, get_data_source)

    # Only update if the resolved reference has id (since it can point to a document that are contained in another document)
    if link_or_storage_address["type"] == SIMOS.LINK.value and "_id" in document:
        # For supporting ^ references, update the current document id
        current_id = document["_id"]

    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return document
    depth_count += 1

    return resolve_document(document, data_source, get_data_source, current_id, depth, depth_count)


def resolve_contained_dict(
    a_dict: dict,
    data_source: DataSource,
    get_data_source,
    current_id: str,
    depth: int = 999,
    depth_count: int = 0,
) -> dict:
    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return a_dict
    depth_count += 1
    entity: dict = a_dict

    return resolve_document(entity, data_source, get_data_source, current_id, depth, depth_count)


def resolve_document(entity, data_source, get_data_source, current_id, depth: int = 999, depth_count: int = 0) -> dict:
    for key, value in entity.items():
        if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
            if not value:
                continue
            if isinstance(value, list):  # If it's a list, resolve any references
                entity[key] = resolve_reference_list(
                    value, data_source, get_data_source, current_id, depth, depth_count
                )
            else:
                if is_reference(value):
                    entity[key] = get_complete_sys_document(
                        value, data_source, get_data_source, current_id, depth, depth_count
                    )
                else:
                    entity[key] = resolve_contained_dict(
                        value, data_source, get_data_source, current_id, depth, depth_count
                    )

    return entity
