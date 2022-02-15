from typing import Callable, List

from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import SIMOS
from utils.exceptions import ValidationException
from utils.string_helpers import get_data_type_from_dmt_type


def valid_extended_type(type: str, extended_types: List[str], get_blueprint: Callable) -> bool:
    if type == SIMOS.ENTITY.value:
        return True
    if type in extended_types:
        return True
    for inherited_type in extended_types:
        blueprint = get_blueprint(inherited_type)
        if type in blueprint.extends:
            return True
        if valid_extended_type(type, blueprint.extends, get_blueprint):
            return True


def entity_has_all_required_attributes(entity: dict, required_attributes: List[BlueprintAttribute]):
    for attribute in required_attributes:
        if attribute.name not in entity:
            raise ValidationException(f"Required attribute '{attribute.name}' not found in the entity")
        if attribute.dimensions.dimensions[0] != "":
            if type(entity[attribute.name]) != list:
                raise ValidationException(
                    f"The type of the required attribute '{attribute.name}' is not correct! It should be a list"
                )
        else:
            attribute_type = get_data_type_from_dmt_type(attribute.attribute_type)
            attribute_type_in_entity = type(entity[attribute.name])
            if attribute.is_primitive() and attribute_type_in_entity != attribute_type:
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
            if not attribute.is_primitive() and type(entity[attribute.name]) != dict:
                raise ValidationException(
                    f"The type of the non-primitive required attribute '{attribute.name}' is not correct!"
                )
