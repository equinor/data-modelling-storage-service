from typing import List

from authentication.models import User
from common.exceptions import NotFoundException
from common.utils.get_document_by_path import get_root_package
from common.utils.string_helpers import split_dmss_ref
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source


def concat_meta_data(meta: dict | None, new_meta: dict | None) -> dict:
    if not meta and not new_meta:
        return {}
    if not meta:
        return new_meta
    if not new_meta:
        return meta

    meta["version"] = new_meta.get("version", meta["version"])
    meta["type"] = new_meta.get("type", meta["type"])
    dependencies = {value["alias"]: value for value in meta["dependencies"]}

    dependencies.update({value["alias"]: value for value in new_meta["dependencies"]})
    meta["dependencies"] = [v for v in dependencies.values()]
    return meta


def _collect_entity_meta_by_path(
    package: dict, path_elements: List[str], data_source: DataSource, existing_meta: dict
) -> dict:
    # TODO: Handle dotted attribute path
    if len(path_elements) == 1:
        target = path_elements[0]
        file = next((f for f in package["content"] if f.get("name", f.get("_id")) == target), None)
        if not file:
            raise NotFoundException(f"The document '{target}' could not be found in the package '{package['name']}'")
        entity: dict = data_source.get(file["_id"])
        return concat_meta_data(existing_meta, entity.get("_meta_"))

    next_package_ref = next((p for p in package["content"] if p["name"] == path_elements[0]), None)
    if not next_package_ref:
        raise NotFoundException(f"The package {path_elements[0]} could not be found in the package {package['name']}")
    next_package: dict = data_source.get(next_package_ref["_id"])
    if not next_package:
        raise NotFoundException(
            f"Could not find package '{next_package_ref['_id']}' in '{data_source.name}/{package['name']}'"
        )
    del path_elements[0]
    collected_meta = concat_meta_data(existing_meta, next_package.get("_meta_"))
    return _collect_entity_meta_by_path(next_package, path_elements, data_source, collected_meta)


def export_meta_use_case(user: User, document_reference: str) -> dict:
    data_source_id, path, attribute = split_dmss_ref(document_reference)
    repository = get_data_source(data_source_id, user)

    path_elements = path.split("/")
    root_package_name = path_elements.pop(0)
    root_package = get_root_package(root_package_name, repository)

    meta = _collect_entity_meta_by_path(root_package, path_elements, repository, root_package.get("_meta_"))
    return meta
