from common.exceptions import NotFoundException


def get_nested_dict_attribute(entity: dict | list, path_list: list[str]) -> dict | list:
    try:
        if isinstance(entity, list):
            path_list[0] = int(path_list[0])  # type: ignore
        if len(path_list) == 1:
            return entity[path_list[0]]  # type: ignore
        return get_nested_dict_attribute(entity[path_list[0]], path_list[1:])  # type: ignore
    except (KeyError, IndexError):
        raise NotFoundException(f"Attribute/Item '{path_list[0]}' does not exists in '{entity}'")
