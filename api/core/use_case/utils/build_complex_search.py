from typing import Callable, Dict

from api.classes.blueprint import Blueprint
from api.classes.blueprint_attribute import BlueprintAttribute
from api.core.repository.repository_exceptions import InvalidAttributeException, RepositoryException


def build_mongo_query(get_blueprint: Callable, search_data: Dict) -> Dict:
    type = search_data.pop("type")
    blueprint: Blueprint = get_blueprint(type)
    # Raise error if posted attribute not in blueprint
    if invalid_type := next((key for key in search_data.keys() if key not in blueprint.get_attribute_names()), None):
        raise InvalidAttributeException(invalid_type, type)

    # The entities 'type' must match exactly
    process_search_data = {"type": type}

    # TODO: This is limited to mongoDB repositories
    # TODO: Does not work with lists in any way
    for key, search_value in search_data.items():
        attribute: BlueprintAttribute = blueprint.get_attribute_by_name(key)

        if attribute.is_array():
            raise RepositoryException("Searching on list attributes are not supported.")

        if search_value == "":
            continue

        if attribute.attribute_type == "string":
            process_search_data[key] = {"$regex": f".*{search_value}.*", "$options": "i"}
            continue

        if not attribute.is_primitive():
            search_value["type"] = attribute.attribute_type
            search_dict = get_complex_search_dict(key, search_value, get_blueprint)
            process_search_data.update(search_dict)
            continue

        if attribute.attribute_type in ["number", "integer"]:
            if search_value[0] == ">":
                process_search_data[key] = {"$gt": float(search_value[1:])}
                continue
            if search_value[0] == "<":
                process_search_data[key] = {"$lt": float(search_value[1:])}
                continue
            process_search_data[key] = float(search_value)

    return process_search_data


def get_complex_search_dict(nested_key: str, search_value: Dict, get_blueprint) -> Dict:
    processed_query = build_mongo_query(get_blueprint, search_value)
    nested_query = {}
    for key, value in processed_query.items():
        nested_query[f"{nested_key}.{key}"] = value
    return nested_query
