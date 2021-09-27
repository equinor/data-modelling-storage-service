import re
from typing import Tuple, Union

from enums import PrimitiveDataTypes


def split_absolute_ref(reference: str) -> Tuple[str, str, str]:
    data_source, dotted_path = reference.split("/", 1)
    attribute = ""
    path = dotted_path
    if "." in dotted_path:  # Dotted path has a attribute reference.
        path, attribute = dotted_path.split(".", 1)
    return data_source, path, attribute


def get_package_and_path(reference: str) -> Tuple[str, Union[list, None]]:
    elements = reference.split("/")
    package = elements.pop(0)
    if len(elements) == 0:
        return package, None
    return package, elements


# Convert dmt attribute_types to python types. If complex, return type as string.
def get_data_type_from_dmt_type(attribute_type: str):
    try:
        type_enum = PrimitiveDataTypes(attribute_type)
        return type_enum.to_py_type()
    except ValueError:
        return attribute_type
    except Exception as error:
        raise Exception(f"Something went wrong trying to fetch data type: {error}")


def url_safe_name(name: str) -> bool:
    # Only allows alphanumeric, underscore, and dash
    expression = re.compile("^[A-Za-z0-9_-]*$")
    match = expression.match(name)
    if match:
        return True
