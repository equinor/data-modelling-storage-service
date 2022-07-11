from typing import List

from utils.exceptions import InvalidSortByAttributeException


def get_value_from_attribute_spec(doc: dict, attribute_path_elements: List[str]):
    for attr_key in attribute_path_elements:
        try:
            # Convert to int if data is a list, and attr_key is numeric
            if isinstance(doc, list):
                if attr_key.isnumeric():
                    attr_key = int(attr_key)
            val = doc[attr_key]
        except KeyError:
            raise InvalidSortByAttributeException(attr_key, doc["type"])

        # Return value if its type is comparable
        if type(val) in [str, int, float, bool]:
            return val

        doc = val


def sort_dtos_by_attribute(entity_list: List[dict], dotted_attribute_path: str) -> List[dict]:
    attribute_path_elements = dotted_attribute_path.split(".")
    entity_list.sort(key=lambda doc: get_value_from_attribute_spec(doc, attribute_path_elements))
    return entity_list
