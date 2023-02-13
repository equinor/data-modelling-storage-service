from typing import Callable, List

from common.exceptions import ValidationException
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import BuiltinDataTypes


def valid_complex_type(valid_type: str, extended_types: List[str], get_blueprint: Callable) -> bool:
    if valid_type == BuiltinDataTypes.OBJECT.value:
        return True
    if valid_type in extended_types:
        return True
    for inherited_type in extended_types:
        inherited_blueprint = get_blueprint(inherited_type)
        if valid_type in inherited_blueprint.extends:
            return True
        if valid_complex_type(valid_type, inherited_blueprint.extends, get_blueprint):
            return True
    return False


def _recursive_validate_single_attribute(
    attribute: BlueprintAttribute, value: dict | bool | int | float | str, get_blueprint: Callable, key: str
):
    debug_message = f"Location: Entity in key '{key}'"
    if attribute.is_primitive:
        python_type = BuiltinDataTypes(attribute.attribute_type).to_py_type()
        if not isinstance(value, python_type):
            raise ValidationException(
                f"Attribute '{attribute.name}' should be type '{python_type.__name__}'. Got '{type(value).__name__}'",
                debug=debug_message,
            )
        if not attribute.is_optional:
            if python_type == str and value == "":
                raise ValidationException(f"Missing required attribute '{attribute.name}'", debug=debug_message)

        return
    if not attribute.is_optional and not value:
        raise ValidationException(f"Missing required attribute '{attribute.name}'", debug=debug_message)

    # Optional empty values are valid
    if not value:
        return

    validate_entity(value, get_blueprint(attribute.attribute_type), get_blueprint, key)  # type: ignore


def validate_entity(
    entity: dict | list, blueprint: Blueprint, get_blueprint: Callable[..., Blueprint], key: str = "^"
) -> None:
    """
    Takes a list, or a complex entity (dict) and validates the entity according to the type of the blueprint.

    Will raise detailed "ValidationException"s if the entity is invalid
    """
    debug_message = f"Location: Entity in key '{key}'"
    if isinstance(entity, list):
        # TODO: Check that dimensions is correct
        for i, item in enumerate(entity):
            validate_entity(item, blueprint, get_blueprint, f"{key}.{i}")
        return

    if not valid_complex_type(blueprint.path, [entity["type"]] + blueprint.extends, get_blueprint):
        raise ValidationException(
            f"Entity should be of type '{blueprint.path}' (or extending from it). Got '{entity['type']}'",
            debug=debug_message,
        )

    # We now know it's a valid child type in entity.
    # Get new, potentially specialized blueprint, from type defined in entity.
    blueprint = get_blueprint(entity["type"])

    if keys_not_in_blueprint := [
        key for key in entity.keys() if key not in blueprint.get_attribute_names() and key != "_id"
    ]:
        raise ValidationException(
            f"Attributes '{keys_not_in_blueprint}' are not specified in the '{blueprint.path}'", debug=debug_message
        )

    for attribute in blueprint.get_required_attributes():
        if entity.get(attribute.name, None) is None and not attribute.is_array:
            raise ValidationException(f"Missing required attribute '{attribute.name}'", debug=debug_message)

    for attribute in [blueprint.get_attribute_by_name(key) for key in entity.keys() if key != "_id"]:
        if attribute.is_array:
            if type(entity[attribute.name]) != list:
                raise ValidationException(f"'{attribute.name}' should be a list", debug=debug_message)
            for i, item in enumerate(entity[attribute.name]):
                if attribute.is_primitive:
                    _recursive_validate_single_attribute(attribute, item, get_blueprint, f"{key}.{attribute.name}.{i}")
                    continue
                validate_entity(
                    item, get_blueprint(attribute.attribute_type), get_blueprint, f"{key}.{attribute.name}.{i}"
                )
            continue

        _recursive_validate_single_attribute(
            attribute, entity[attribute.name], get_blueprint, f"{key}.{attribute.name}"
        )
