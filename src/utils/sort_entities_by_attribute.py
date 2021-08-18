from typing import List

from domain_classes.dto import DTO
from utils.exceptions import InvalidSortByAttributeException


def get_value_from_attribute_spec(doc: DTO, attribute_path_elements: List[str]):
    data = doc.data
    for attr_key in attribute_path_elements:
        try:
            # Convert to int if data is a list, and attr_key is numeric
            if isinstance(data, list):
                if attr_key.isnumeric():
                    attr_key = int(attr_key)
            val = data[attr_key]
        except KeyError:
            raise InvalidSortByAttributeException(attr_key, data["type"])

        # Return value if its type is comparable
        if type(val) in [str, int, float, bool]:
            return val

        data = val


def sort_dtos_by_attribute(dto_list: List[DTO], dotted_attribute_path: str) -> List[DTO]:
    attribute_path_elements = dotted_attribute_path.split(".")
    dto_list.sort(key=lambda doc: get_value_from_attribute_spec(doc, attribute_path_elements))
    return dto_list
