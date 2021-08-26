from domain_classes.dto import DTO
from storage.data_source_class import DataSource


def resolve_reference_list(x: list, document_repository: DataSource) -> list:
    if not x:  # Return an empty list
        return x
    resolved = []

    if isinstance(x[0], list):  # Call recursively for nested lists
        resolved = [resolve_reference_list(item, document_repository) for item in x]
    for value in x:
        if isinstance(value, dict) and value.get("_id"):  # It's a reference!
            resolved.append(get_complete_document(value["_id"], document_repository))
        else:
            resolved.append(value)
    return resolved


def get_complete_document(document_uid: str, data_source: DataSource, depth: int = 999, depth_count: int = 0,) -> dict:
    document: DTO = data_source.get(str(document_uid))
    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return document.data
    depth_count += 1
    entity: dict = document.data
    for key, value in entity.items():
        if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
            if not value:
                continue
            if isinstance(value, list):  # If it's a list, resolve any references
                entity[key] = resolve_reference_list(value, data_source)
            else:
                value: dict
                if ref_id := value.get("_id"):  # It's a reference
                    entity[key] = get_complete_document(ref_id, data_source, depth_count)

    return entity
