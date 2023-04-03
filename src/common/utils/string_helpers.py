import re
from typing import Tuple, Union

from enums import BuiltinDataTypes

# Some terminology;

# PATH_REFERENCE = datasource/package/folder/entity.attribute
# ID_REFERENCE = datasource/uid.attribute
# DOTTED_PATH = package/folder/entity.attribute
# DOTTED_ID = uid.attribute

# DMSS_REFERENCE = {PATH_REFERENCE, ID_REFERENCE}
# ABSOLUTE_REFERENCE = PROTOCOL://ADDRESS


def split_dmss_ref(dmss_reference: str) -> Tuple[Union[str, None], Union[str, None], Union[str, None]]:
    """Will split 'path_references' and 'id_references' into it's 3 parts."""
    if dmss_reference.startswith("/"):  # By root (no specified data source)
        # Expects format: //(PATH|ID).Attribute
        dmss_reference = dmss_reference.strip("/. ")  # Remove leading and trailing stuff
        document_id, attributes = split_dotted_id(dmss_reference)
        return None, document_id, attributes
    else:  # By data source
        # Expects format: /DATA_SOURCE/(PATH|ID).Attribute
        dmss_reference = dmss_reference.strip("/. ")  # Remove leading and trailing stuff
        if "/" not in dmss_reference:  # It's reference to the data_source itself
            return dmss_reference, None, None
        data_source, dotted_id = dmss_reference.split("/", 1)
        document_id, attributes = split_dotted_id(dotted_id)
        return data_source, document_id, attributes


def split_dotted_id(dotted_id: str) -> Tuple[str, str | None]:
    if "." not in dotted_id:  # No attribute path in the id
        return dotted_id, None
    return dotted_id.split(".", 1)  # type: ignore


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
    return False
