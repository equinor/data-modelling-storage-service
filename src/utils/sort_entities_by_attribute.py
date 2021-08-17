from typing import List

from domain_classes.dto import DTO
from utils.exceptions import InvalidAttributeException


def get_value_from_attribute_spec(doc: DTO, attribute_spec: List[str]):
    data = doc.data
    for attr_key in attribute_spec:
        try:
            val = data[attr_key]
        except KeyError:
            raise InvalidAttributeException(attr_key, data["type"])

        if not isinstance(val, dict):
            return val

        data = val


def sort_dtos_by_attribute(dto_list: List[DTO], dotted_attribute_path: str) -> List[DTO]:
    attribute_path_elements = sort_by_attribute.split(".")
    result_list.sort(key=lambda doc: get_value_from_attribute_spec(doc, attribute_spec))
    return result_list
