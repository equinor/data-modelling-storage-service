from common.exceptions import BadRequestException


def _get_value_from_attribute_spec(document: dict, attribute_path_elements: list[str]):
    for attr_key in attribute_path_elements:
        try:
            # Convert to int if data is a list, and attr_key is numeric
            if isinstance(document, list):
                if attr_key.isnumeric():
                    attr_key = int(attr_key)
            val = document[attr_key]
        except KeyError as ex:
            raise BadRequestException(f"'{attr_key}' is not a valid attribute in the '{document['type']}'") from ex

        # Return value if its type is comparable
        if type(val) in [str, int, float, bool]:
            return val

        document = val


def sort_dtos_by_attribute(entity_list: list[dict], dotted_attribute_path: str) -> list[dict]:
    attribute_path_elements = dotted_attribute_path.split(".")
    entity_list.sort(key=lambda document: _get_value_from_attribute_spec(document, attribute_path_elements))
    return entity_list
