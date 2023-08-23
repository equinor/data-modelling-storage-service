import math

from domain_classes.dependency import Dependency


def has_dependency_alias(reference: str, dependencies: list[Dependency]) -> bool:
    """Check if a given reference string on the format <protocol>://<datasource>/<path> can be
    substituted with an alias on the format <alias>:<path>.
    """
    for dependency in dependencies:
        if reference.startswith(dependency.get_prefix()):
            return True
    return False


def replace_reference_with_alias_if_possible(reference: str, dependencies: list[Dependency]) -> str | None:
    """Replace the reference string with an alias.
    The reference string on the format <protocol>://<datasource>/<path>.

    If the reference does not have an alias that match, the original reference is returned.
    """
    if not has_dependency_alias(reference, dependencies):
        return reference
    best_alias_match = None
    longest_path_length_after_alias = math.inf
    for dependency in dependencies:
        if reference.startswith(dependency.get_prefix()):
            path_after_alias = reference.split(dependency.get_prefix())[-1]
            if len(path_after_alias) < longest_path_length_after_alias:
                best_alias_match = f"{dependency.alias}:{path_after_alias}"
                longest_path_length_after_alias = len(path_after_alias)
    return best_alias_match


def replace_absolute_references_in_entity_with_alias(entity: dict, dependencies: list[Dependency]) -> dict:
    """Replace references (<protocol>://<datasource>/<path>) in an entity with aliases (<alias>:<path>)
     defined in a list of dependencies.

    (for example, replace "dmss://system/SIMOS/Package" with "CORE:Package".)
    """
    attributes_to_update = ("type", "attributeType", "_blueprintPath_")  # These keys may contain a reference
    EXTENDS = "extends"  # Extends is a special attribute in an entity that contains a list of references

    for attribute, attribute_value in entity.items():
        if attribute == EXTENDS:
            entity[EXTENDS] = [
                replace_reference_with_alias_if_possible(reference, dependencies) for reference in attribute_value
            ]
        elif attribute in attributes_to_update:
            entity[attribute] = replace_reference_with_alias_if_possible(attribute_value, dependencies)
        elif isinstance(attribute_value, dict):
            entity[attribute] = replace_absolute_references_in_entity_with_alias(attribute_value, dependencies)
        elif isinstance(attribute_value, list):
            for index, new_entity in enumerate(attribute_value):
                if isinstance(new_entity, dict):
                    entity[attribute][index] = replace_absolute_references_in_entity_with_alias(
                        new_entity, dependencies
                    )
    return entity
