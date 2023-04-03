from typing import Tuple, Union

from common.utils.get_document_by_path import get_document_uid_by_path
from common.utils.get_nested_dict_attribute import get_nested_dict_attribute
from common.utils.string_helpers import split_dmss_ref
from enums import SIMOS
from storage.data_source_class import DataSource


def is_reference(entity):
    return isinstance(entity, dict) and (
        entity.get("type") == SIMOS.STORAGE_ADDRESS.value or entity.get("type") == SIMOS.LINK.value
    )


def resolve_reference_list(x: list, document_repository: DataSource, depth: int = 999, depth_count: int = 0) -> list:
    if not x:  # Return an empty list
        return x
    resolved: list[dict | list] = []

    if isinstance(x[0], list):  # Call recursively for nested lists
        resolved = [resolve_reference_list(item, document_repository) for item in x]
    for value in x:
        if is_reference(value):
            resolved.append(get_complete_sys_document(value["ref"], document_repository, depth, depth_count))
        elif isinstance(value, dict):
            resolved.append(resolve_contained_dict(value, document_repository, depth, depth_count))
        else:
            resolved.append(value)
    return resolved


def resolve_reference(reference: str, data_source) -> Tuple[Union[str, None], Union[str, None]]:
    """Resolve the reference into data_source_id, document_id, and attribute."""
    if "://" in reference:
        """
        Supported formats:
        - Absolute: PROTOCOL://DATA_SOURCE/(PATH|ID).ATTRIBUTE
        - Root:     PROTOCOL:///(PATH|ID).ATTRIBUTE
        """
        protocol, dmss_reference = reference.split("://", 1)
        match protocol:
            case "dmss":
                data_source_id, id_or_path, attribute = split_dmss_ref(dmss_reference)
                if "/" in id_or_path:  # By path
                    document_id = get_document_uid_by_path(id_or_path, data_source)
                else:  # By id
                    document_id = id_or_path
                return document_id, attribute
            case _:
                raise Exception(f"The protocol '{protocol}' is not supported")
    else:  # Only id
        return reference, None


def get_complete_sys_document(
    dmss_reference: str,
    data_source: DataSource,
    depth: int = 999,
    depth_count: int = 0,
) -> dict:
    document_id, attribute = resolve_reference(dmss_reference, data_source)

    document: dict = data_source.get(document_id)

    if attribute:
        document = get_nested_dict_attribute(document, attribute.split("."))

    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return document
    depth_count += 1

    return resolve_complete_document(document, data_source, depth, depth_count)


def resolve_contained_dict(
    a_dict: dict,
    data_source: DataSource,
    depth: int = 999,
    depth_count: int = 0,
) -> dict:
    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return a_dict
    depth_count += 1
    entity: dict = a_dict

    return resolve_complete_document(entity, data_source, depth, depth_count)


def resolve_complete_document(entity, data_source, depth, depth_count) -> dict:
    for key, value in entity.items():
        if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
            if not value:
                continue
            if isinstance(value, list):  # If it's a list, resolve any references
                entity[key] = resolve_reference_list(value, data_source, depth, depth_count)
            else:
                if ref := is_reference(value) and value.get("ref"):
                    entity[key] = get_complete_sys_document(ref, data_source, depth, depth_count)
                else:
                    entity[key] = resolve_contained_dict(value, data_source, depth, depth_count)

    return entity
