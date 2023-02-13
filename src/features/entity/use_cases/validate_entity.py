from typing import Callable

from pydantic import BaseModel
from pydantic.config import Extra

from authentication.models import User
from common.exceptions import ValidationException
from common.utils.validators import valid_complex_type
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import BuiltinDataTypes
from restful.request_types.shared import common_type_constrained_string
from services.document_service import DocumentService


class BasicEntity(BaseModel, extra=Extra.allow):
    type: common_type_constrained_string  # type: ignore


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
        if not valid_complex_type(blueprint.path, [entity["type"]] + blueprint.extends, get_blueprint):
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


def validate_entity_use_case(entity: BasicEntity, user: User, as_type: common_type_constrained_string | None) -> str:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(as_type if as_type else entity.type)
    validate_entity(entity.dict(), blueprint, document_service.get_blueprint, allow_extra=bool(as_type))
    return "OK"
