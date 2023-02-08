from typing import Callable, List

from common.exceptions import ValidationException
from common.utils.logging import logger
from common.utils.string_helpers import get_data_type_from_dmt_type
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
