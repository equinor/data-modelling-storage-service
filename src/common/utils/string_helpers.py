import re

# Some terminology;

# PATH_REFERENCE = datasource/package/folder/entity.attribute
# ID_REFERENCE = datasource/uid.attribute
# DOTTED_PATH = package/folder/entity.attribute
# DOTTED_ID = uid.attribute

# DMSS_REFERENCE = {PATH_REFERENCE, ID_REFERENCE}
# ABSOLUTE_REFERENCE = PROTOCOL://ADDRESS


def url_safe_name(name: str) -> bool:
    # Only allows alphanumeric, underscore, and dash
    expression = re.compile("^[A-Za-z0-9_-]*$")
    match = expression.match(name)
    if match:
        return True
    return False
