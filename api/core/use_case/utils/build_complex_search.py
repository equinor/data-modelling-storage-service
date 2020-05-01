from typing import Callable, Dict, List

from api.classes.blueprint import Blueprint
from api.classes.blueprint_attribute import BlueprintAttribute
from api.core.repository.repository_exceptions import InvalidAttributeException, RepositoryException


def attribute_to_mongo_query(attribute: BlueprintAttribute, search_value: Dict, key: str, get_blueprint: Callable):
    # Lists
    # TODO: Can now only
    if isinstance(search_value, List):
        if attribute.is_primitive():
            return attribute_to_mongo_query(attribute, search_value[0], key, get_blueprint)
        else:
            list_search_value = search_value[0]
            list_search_value["type"] = attribute.attribute_type
            search_dict = get_complex_search_dict(key, list_search_value, get_blueprint)
            return search_dict

    # Empty attributes will be stripped
    if search_value == "":
        return

    # Strings
    if attribute.attribute_type == "string":
        return {"$regex": f".*{search_value}.*", "$options": "i"}

    # Numbers
    if attribute.attribute_type in ["number", "integer"]:
        if search_value[0] == ">":
            return {"$gt": float(search_value[1:])}
        if search_value[0] == "<":
            return {"$lt": float(search_value[1:])}

        return float(search_value)

    # Complex
    if not attribute.is_primitive():
        search_value["type"] = attribute.attribute_type
        return get_complex_search_dict(key, search_value, get_blueprint)


def build_mongo_query(get_blueprint: Callable, search_data: Dict) -> Dict:
    type = search_data.pop("type")
    blueprint: Blueprint = get_blueprint(type)
    # Raise error if posted attribute not in blueprint
    if invalid_type := next((key for key in search_data.keys() if key not in blueprint.get_attribute_names()), None):
        raise InvalidAttributeException(invalid_type, type)

    # The entities 'type' must match exactly
    process_search_data = {"type": type}

    for key, search_value in search_data.items():
        attribute: BlueprintAttribute = blueprint.get_attribute_by_name(key)

        if attribute.is_primitive():
            process_search_data[key] = attribute_to_mongo_query(attribute, search_value, key, get_blueprint)
        else:
            process_search_data.update(attribute_to_mongo_query(attribute, search_value, key, get_blueprint))

    return process_search_data


def get_complex_search_dict(nested_key: str, search_value: Dict, get_blueprint) -> Dict:
    processed_query = build_mongo_query(get_blueprint, search_value)
    nested_query = {}
    for key, value in processed_query.items():
        nested_query[f"{nested_key}.{key}"] = value
    return nested_query
