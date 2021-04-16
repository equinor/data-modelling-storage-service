import re
from typing import Tuple, Union

from enums import PrimitiveDataTypes


def get_data_source_and_path(reference: str) -> Tuple[str, str]:
    ref_elements = reference.split("/", 1)
    if len(ref_elements) <= 1:
        raise Exception(f"Invalid reference: {reference}")
    return ref_elements[0], ref_elements[1]


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
