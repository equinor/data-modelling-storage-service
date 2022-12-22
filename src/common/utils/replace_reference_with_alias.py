from common.exceptions import ApplicationException
from domain_classes.dependency import Dependency


def is_alias(string_to_check: str, dependencies: list[Dependency]) -> bool:
    """Check if a given string is an alias or not.

    string_to_check is an alias on the form <alias>:<path> or a document reference on the format <protocol>://<datasource>/<path>
    """
    for dependency in dependencies:
        if (
            string_to_check.startswith(f"{dependency.alias}:")
            and dependency.protocol not in string_to_check
            and dependency.address not in string_to_check
        ):
            return True
    return False


def replace_reference_with_alias(reference: str, dependencies: list[Dependency]) -> str:
    """
    replace the reference string with an alias.
    The reference string on the format <protocol>://<datasource>/<path>.
    """
    for dependency in dependencies:
        if reference.startswith(dependency.get_absolute_reference()):
            path_after_alias = reference.split(dependency.get_absolute_reference())[-1]
            return f"{dependency.alias}:{path_after_alias}"
    raise ApplicationException(
        message="Could not replace reference with alias",
        debug=f"reference: {reference} could not be replaced with alias.",
    )


def replace_absolute_references_in_entity_with_alias(entity: dict, dependencies: list[Dependency]):
    """Replace path in an entity with alias defined in a list of dependencies.

    (for example, replace "dmss://system/SIMOS/Package" with "CORE:Package".)
    """
    attributes_to_update = ("type", "attributeType", "_blueprintPath_")  # These keys may contain a reference
    EXTENDS = "extends"  # extends is a special attribute in an entity that contains a list of referencences
    for attribute in entity:
        if type(entity[attribute]) == list and attribute != EXTENDS:
            for new_entity in entity[attribute]:
                replace_absolute_references_in_entity_with_alias(new_entity, dependencies)
        if attribute in attributes_to_update:
            entity[attribute] = replace_reference_with_alias(entity[attribute], dependencies)
        elif attribute == EXTENDS:
            for index, reference in enumerate(entity[attribute]):
                if not is_alias(reference, dependencies):
                    entity[attribute][index] = replace_reference_with_alias(entity[attribute][index], dependencies)
