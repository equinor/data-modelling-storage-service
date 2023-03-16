from typing import Callable, List

from common.exceptions import ValidationException
from common.utils.logging import logger
from common.utils.string_helpers import get_data_type_from_dmt_type
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import BuiltinDataTypes


def is_blueprint_instance_of(
    minimum_blueprint_type: str, blueprint_type: str, get_blueprint: Callable[..., Blueprint]
) -> bool:
    """Takes in a blueprint and checks if it's an instance of a minimum blueprint

    Args:
        minimum_blueprint_type: Blueprint to validate against
        blueprint_type: Blueprint to validate

    Returns:
        bool:
            Returns true if:
                the minimum blueprint has the generic "object" type, since all blueprints are objects
                the blueprint has the same type as the minimum blueprint
                the blueprint extends a blueprint that fulfills one of these three rules
            Otherwise it returns false.
    """
    if minimum_blueprint_type == BuiltinDataTypes.OBJECT.value:
        return True
    if minimum_blueprint_type == blueprint_type:
        return True
    for inherited_type in get_blueprint(blueprint_type).extends:
        if is_blueprint_instance_of(minimum_blueprint_type, inherited_type, get_blueprint):
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
    entity: dict | list,
    blueprint: Blueprint,
    get_blueprint: Callable[..., Blueprint],
    key: str = "^",
    allow_extra: bool = False,
) -> None:
    """Takes a list, or a complex entity (dict) and validates the entity according to the type of the blueprint.

    Args:
        blueprint: Blueprint to check the entity against
        key: Dotted path to the location of the current entity.
        allow_extra: Whether to raise ValidationException on keys in entity not defined in blueprint

    Raises:
        Will raise detailed "ValidationException"s if the entity is invalid
    """
    debug_message = f"Location: Entity in key '{key}'"
    if isinstance(entity, list):
        # TODO: Check that dimensions is correct
        for i, item in enumerate(entity):
            validate_entity(item, blueprint, get_blueprint, f"{key}.{i}")
        return

    if not allow_extra:
        if not is_blueprint_instance_of(blueprint.path, entity["type"], get_blueprint):
            raise ValidationException(
                f"Entity should be of type '{blueprint.path}' (or extending from it). Got '{entity['type']}'",
                debug=debug_message,
            )

        # We now know it's a valid child type in entity.
        # Get new, potentially specialized blueprint, from type defined in entity.
        blueprint = get_blueprint(entity["type"])

        if keys_not_in_blueprint := [key for key in entity.keys() if key not in blueprint.get_attribute_names()]:
            raise ValidationException(
                f"Attributes '{keys_not_in_blueprint}' are not specified in the '{blueprint.path}'",
                debug=debug_message,
            )

    for attribute in blueprint.get_required_attributes():
        if entity.get(attribute.name, None) is None and not attribute.is_array:
            raise ValidationException(f"Missing required attribute '{attribute.name}'", debug=debug_message)

    for attribute in [blueprint.get_attribute_by_name(key) for key in entity.keys()]:
        if attribute is None:
            continue
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


def entity_has_all_required_attributes(entity: dict, required_attributes: List[BlueprintAttribute]):
    for attribute in required_attributes:
        if attribute.name not in entity:
            logger.warning(entity)
            raise ValidationException(f"Required attribute '{attribute.name}' not found in the entity")
        if attribute.dimensions.dimensions[0] != "":
            if type(entity[attribute.name]) != list:
                raise ValidationException(
                    f"The type of the required attribute '{attribute.name}' is not correct! It should be a list"
                )
        else:
            attribute_type = get_data_type_from_dmt_type(attribute.attribute_type)
            attribute_type_in_entity = type(entity[attribute.name])
            if attribute.is_primitive and attribute_type_in_entity != attribute_type:
                # the validation will accept cases where the type in the blueprint is defined to be integer, but
                # the value in the entity has zero in the decimal place.
                if attribute_type == int and attribute_type_in_entity == float:
                    if not entity[attribute.name].is_integer():
                        raise ValidationException(
                            f"The type of the required primitive attribute '{attribute.name}' is not correct!"
                        )
                elif attribute_type == float and attribute_type_in_entity == int:
                    return
                else:
                    raise ValidationException(
                        f"The type of the required primitive attribute '{attribute.name}' is not correct!"
                    )
            if not attribute.is_primitive and type(entity[attribute.name]) != dict:
                raise ValidationException(
                    f"The type of the non-primitive required attribute '{attribute.name}' is not correct!"
                )
