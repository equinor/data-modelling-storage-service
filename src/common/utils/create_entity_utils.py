import string
from random import choices

from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import BuiltinDataTypes
from common.utils.string_helpers import get_data_type_from_dmt_type


def generate_name(type: str) -> str:
    name_of_type: str = type.split("/")[-1]
    lower_case_type_name: str = name_of_type.lower()
    # This random string generation is not used in a cryptographic manner, so disable bandit warning
    random_suffix: str = "".join(choices(string.ascii_lowercase + string.digits, k=4))  # nosec B311
    return f"{lower_case_type_name}-{random_suffix}"


def set_default(attr: BlueprintAttribute, blueprint_provider):
    if attr.is_array:
        return attr.dimensions.create_default_array(blueprint_provider, attr)

    if attr.default:
        if attr.is_primitive:
            # Convert default value to correct type
            return get_data_type_from_dmt_type(attr.attribute_type)(attr.default)
        return attr.default

    # Setting default, default values...
    match attr.attribute_type:
        case "boolean":
            return False
        case "number":
            return 0.0
        case "string":
            return ""
        case "integer":
            return 0


def create_entity(blueprint_provider, entity: dict) -> dict:
    if entity["type"] == BuiltinDataTypes.OBJECT.value:  # Can't create entities of unknown type 'object'
        return {}
    blueprint: Blueprint = blueprint_provider(entity["type"])

    for attr in blueprint.attributes:
        if attr.is_primitive and not attr.is_array:
            if attr.attribute_type == "string" and attr.name == "name":
                entity[attr.name] = entity.get(attr.name, generate_name(entity["type"]))
                continue
            entity[attr.name] = entity.get(attr.name, set_default(attr, blueprint_provider))
            continue
        if attr.is_array:
            entity[attr.name] = attr.dimensions.create_default_array(blueprint_provider, create_entity)
            continue
        # It's complex
        # Can not create entities of unknown 'object' type
        if attr.optional:
            entity[attr.name] = {}
            continue
        entity[attr.name] = create_entity(
            blueprint_provider, {"type": attr.attribute_type, **entity.get(attr.name, {})}
        )

    return entity