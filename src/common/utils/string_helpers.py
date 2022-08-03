import re
from typing import Tuple, Union

from enums import BuiltinDataTypes


def split_absolute_ref(reference: str) -> Tuple[str, Union[str, None], Union[str, None]]:
    reference = reference.strip("/. ")  # Remove leading and trailing stuff
    if "/" not in reference:  # It's reference to the data_source itself
        return reference, None, None
    data_source, dotted_id = reference.split("/", 1)
    document_id, attributes = split_dotted_id(dotted_id)
    return data_source, document_id, attributes


def split_dotted_id(dotted_id: str) -> Tuple[str, Union[str, None]]:
    if "." not in dotted_id:  # No attribute path in the id
        return dotted_id, None
    return dotted_id.split(".", 1)


def get_package_and_path(reference: str) -> Tuple[str, Union[list, None]]:
    elements = reference.split("/")
    package = elements.pop(0)
    if len(elements) == 0:
        return package, None
    return package, elements


# Convert dmt attribute_types to python types. If complex, return type as string.
def get_data_type_from_dmt_type(attribute_type: str):
    try:
        type_enum = BuiltinDataTypes(attribute_type)
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
