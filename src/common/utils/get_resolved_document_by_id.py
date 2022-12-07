from storage.data_source_class import DataSource


def resolve_reference_list(x: list, document_repository: DataSource, depth: int = 999, depth_count: int = 0) -> list:
    if not x:  # Return an empty list
        return x
    resolved: list[dict | list] = []

    if isinstance(x[0], list):  # Call recursively for nested lists
        resolved = [resolve_reference_list(item, document_repository) for item in x]
    for value in x:
        if isinstance(value, dict) and value.get("_id"):  # It's a reference!
            resolved.append(get_complete_sys_document(value["_id"], document_repository, depth, depth_count))
        elif isinstance(value, dict):
            resolved.append(resolve_contained_dict(value, document_repository, depth, depth_count))
        else:
            resolved.append(value)
    return resolved


def get_complete_sys_document(
    document_uid: str,
    data_source: DataSource,
    depth: int = 999,
    depth_count: int = 0,
) -> dict:
    document: dict = data_source.get(str(document_uid))
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
                if ref_id := value.get("_id"):  # It's a reference
                    entity[key] = get_complete_sys_document(ref_id, data_source, depth_count)
                else:
                    entity[key] = resolve_contained_dict(value, data_source, depth, depth_count)

    return entity
