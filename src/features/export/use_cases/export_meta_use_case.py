from authentication.models import User
from common.address import Address
from common.exceptions import NotFoundException
from common.providers.address_resolver.address_resolver import (
    QueryItem,
    path_to_path_items,
    resolve_address,
)
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source


def concat_meta_data(meta: dict | None, new_meta: dict | None) -> dict:
    if not meta and not new_meta:
        return {}
    if not meta:
        return new_meta if new_meta else {}
    if not new_meta:
        return meta

    meta["version"] = new_meta.get("version", meta["version"])
    meta["type"] = new_meta.get("type", meta["type"])
    dependencies = {value["alias"]: value for value in meta["dependencies"]}

    dependencies.update({value["alias"]: value for value in new_meta["dependencies"]})
    meta["dependencies"] = list(dependencies.values())
    return meta


def resolve_references(values: list, data_source: DataSource, user: User) -> list:
    return [
        resolve_address(
            Address.from_relative(value["address"], None, data_source.name),
            lambda data_source_name: get_data_source(data_source_name, user),
        ).entity
        for value in values
    ]


def _collect_entity_meta_by_path(
    package: dict, path_elements: list[str], data_source: DataSource, existing_meta: dict | None, user: User
) -> dict:
    # TODO: Handle dotted attribute path
    if len(path_elements) == 1:
        target = path_elements[0]

        file = next(
            (
                f
                for f in resolve_references(package["content"], data_source, user)
                if f.get("name", f.get("_id")) == target
            ),
            None,
        )
        if not file:
            raise NotFoundException(f"The document '{target}' could not be found in the package '{package['name']}'")
        entity: dict = data_source.get(file["_id"])
        return concat_meta_data(existing_meta, entity.get("_meta_"))

    next_package_ref = next(
        (p for p in resolve_references(package["content"], data_source, user) if p["name"] == path_elements[0]), None
    )
    if not next_package_ref:
        raise NotFoundException(f"The package {path_elements[0]} could not be found in the package {package['name']}")
    next_package: dict = data_source.get(next_package_ref["_id"])
    if not next_package:
        raise NotFoundException(
            f"Could not find package '{next_package_ref['_id']}' in '{data_source.name}/{package['name']}'"
        )
    del path_elements[0]
    collected_meta = concat_meta_data(existing_meta, next_package.get("_meta_"))
    return _collect_entity_meta_by_path(next_package, path_elements, data_source, collected_meta, user)


def export_meta_use_case(user: User, path_address: str) -> dict:
    """Export meta.

    This function assumes that reference is on a path format, without any id.
    Also, a reference must be on the format PROTOCOL://DATASOURCE_NAME/ROOT_PACKAGE/*path to document or package*.
    (Protocol is optional)
    """
    address_object = Address.from_absolute(path_address)

    data_source = get_data_source(address_object.data_source, user)
    if not address_object.path:
        raise NotFoundException(f"Could not find a root package from reference '{path_address}'")
    path_items = path_to_path_items(address_object.path)
    if len(path_items) >= 1 and isinstance(path_items[0], QueryItem) and path_items[0].query_as_dict["isRoot"]:
        root_package_name = path_items[0].query_as_dict["name"]
    else:
        raise NotFoundException(f"Could not find a root package from reference '{path_address}'")

    root_package: dict = resolve_address(
        Address(root_package_name, address_object.data_source),
        lambda data_source_name: get_data_source(data_source_name, user),
    ).entity

    path_without_root_package: list[str] = address_object.path.strip("/").split("/")[1:]

    if not path_without_root_package:
        return root_package.get("_meta_", {})

    meta = _collect_entity_meta_by_path(
        root_package, path_without_root_package, data_source, root_package.get("_meta_"), user
    )
    return meta
