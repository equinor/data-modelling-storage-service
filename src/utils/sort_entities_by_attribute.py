from typing import List

from domain_classes.dto import DTO
from utils.exceptions import InvalidAttributeException


def get_value_from_attribute_spec(doc: DTO, attribute_path_elements: List[str]):
    data = doc.data
    for attr_key in attribute_path_elements:
        try:
            val = data[attr_key]
        except KeyError:
            raise InvalidAttributeException(attr_key, data["type"])

        if not isinstance(val, dict):
            return val

        data = val


def sort_dtos_by_attribute(dto_list: List[DTO], dotted_attribute_path: str) -> List[DTO]:
    attribute_path_elements = dotted_attribute_path.split(".")
    dto_list.sort(key=lambda doc: get_value_from_attribute_spec(doc, attribute_path_elements))
    return dto_list
