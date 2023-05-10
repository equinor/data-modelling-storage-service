import re
from typing import Any


def _get_value(obj: object, key: str):
    match = re.search(r"^\[([0-9]+)\]$", key)
    if isinstance(obj, list) and match:
        return obj[int(match.group(1))]
    if isinstance(obj, dict) and not match:
        return obj[key]

    raise ValueError(f"Invalid path. Object {obj} has no key {key}")


def find(obj: dict | list, path: list[str | list[int]]) -> Any:
    """
    Find a value in a nested object

    :param obj: a nested dict or list. Note that all dict keys must be strings
    :param path: a list, where each element can be either a parameter or an array index. Ex: ["myKey", "[10]", [10]]
    :return: the value the path leads to
    :raise:
        NotFoundException if the path format does not match the type of obj
        IndexError if the list does not have the index requested
        KeyError if the dict does not have the key requested
    """
    result = obj
    for key in path:
        result = _get_value(result, str(key))
    return result
