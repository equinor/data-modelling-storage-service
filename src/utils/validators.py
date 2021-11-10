from typing import Callable, List

from pydantic import ValidationError

from restful.request_types.shared import Entity
from utils.exceptions import InvalidEntityException, ValidationException


def valid_extended_type(type: str, extended_types: List[str], get_blueprint: Callable) -> bool:
    if type in extended_types:
        return True
    for inherited_type in extended_types:
        blueprint = get_blueprint(inherited_type)
        if type in blueprint.extends:
            return True
        if valid_extended_type(type, blueprint.extends, get_blueprint):
            return True


def valid_named_entity(entity: dict) -> None:
    try:  # Minimal check that the child is a valid entity
        Entity(**entity)
    except (ValidationError, TypeError):
        raise InvalidEntityException(f"'{entity}' is not a valid entity.") from None


def entity_has_all_required_attributes(entity: dict, required_attributes: list):
    for attribute in required_attributes:
        if entity != {} and (attribute not in entity):
            raise ValidationException(f"Required attribute '{attribute}' not found in the entity")
    pass
