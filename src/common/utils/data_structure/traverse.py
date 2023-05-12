from common.utils.data_structure.dot_notation import to_dot_notation


def _diff(actual: object, expected: object, path: list[str], message: str):
    return {"expected_value": expected, "path": to_dot_notation(path), "actual_value": actual, "message": message}


def _key_diff(dict1: dict, dict2: dict):
    return ", ".join(set(dict1.keys()) - set(dict2.keys()))


def traverse_compare(actual: dict | list, expected: dict | list) -> list:
    """
    Object properties matcher.

    Usage:
       >>> actual = {"top": {"middle" : {"nested": "value"}}}
       >>> expected = {"top": {"middle" : {"nested": "value"}}}
       >>> traverse_compare(actual, expected)
       []

    :param obj1: The actual object.
    :param obj2: The expected object.
    :return: List of properties that does not match.
    """
    return _traverse(actual, expected, [])


def _traverse(actual: object, expected: object, path: list[str]) -> list[dict]:
    result: list[dict] = []

    if isinstance(actual, dict) and isinstance(expected, dict):
        if set(actual.keys()) != set(expected.keys()):
            message = f"Missing keys: {_key_diff(expected, actual)}. Extra keys: {_key_diff(actual, expected)}"
            result = [_diff(actual, expected, path, message)]
        for key in set(actual.keys()) & set(expected.keys()):
            result += _traverse(actual[key], expected[key], path + [key])
        return result

    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return [_diff(actual, expected, path, f"Actual length: {len(actual)}. Expected length: {len(expected)}")]
        for iterator in range(len(actual)):
            result += _traverse(actual[iterator], expected[iterator], path + [f"[{iterator}]"])
        return result

    if actual != expected:
        return [_diff(actual, expected, path, "Difference in primitive value")]

    return []
