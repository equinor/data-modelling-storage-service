import re

from enums import BuiltinDataTypes

# Some terminology;

# PATH_REFERENCE = datasource/package/folder/entity.attribute
# ID_REFERENCE = datasource/uid.attribute
# DOTTED_PATH = package/folder/entity.attribute
# DOTTED_ID = uid.attribute

# DMSS_REFERENCE = {PATH_REFERENCE, ID_REFERENCE}
# ABSOLUTE_REFERENCE = PROTOCOL://ADDRESS


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
