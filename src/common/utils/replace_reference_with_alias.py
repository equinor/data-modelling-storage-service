import math

from domain_classes.dependency import Dependency


def has_dependency_alias(reference: str, dependencies: list[Dependency]) -> bool:
    """Check if a given reference string on the format <protocol>://<datasource>/<path> can be
    substituted with an alias on the format <alias>:<path>.
    """
    for dependency in dependencies:
        if reference.startswith(dependency.get_absolute_reference()):
            return True
    return False


def replace_references_in_list(reference_list: list[str], dependencies: list[Dependency]) -> list[str]:
    """Replace references with alias of a list with references.

    The reference_list contains a list of references on the format <protocol>://<datasource>/<path>.
    The returned value is a list where all references are substituted with aliases on the format <alias>:<path>.
    """

    list_with_alias = []
    for index, reference in enumerate(reference_list):
        list_with_alias.append(replace_reference_with_alias_if_possible(reference, dependencies))
    return list_with_alias


def replace_reference_with_alias_if_possible(reference: str, dependencies: list[Dependency]) -> str:
    """Replace the reference string with an alias.
    The reference string on the format <protocol>://<datasource>/<path>.

    If the reference does not have an alias that match, the original reference is returned.
    """
    if not has_dependency_alias(reference, dependencies):
        return reference
    best_alias_match = None
    longest_path_length_after_alias = math.inf
    for dependency in dependencies:
        if reference.startswith(dependency.get_absolute_reference()):
            path_after_alias = reference.split(dependency.get_absolute_reference())[-1]
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

    for attribute in entity:
        if attribute == EXTENDS:
            entity[EXTENDS] = replace_references_in_list(reference_list=entity[EXTENDS], dependencies=dependencies)
        elif attribute in attributes_to_update:
            entity[attribute] = replace_reference_with_alias_if_possible(entity[attribute], dependencies)
        elif type(entity[attribute]) == dict:
            entity[attribute] = replace_absolute_references_in_entity_with_alias(entity[attribute], dependencies)
        elif type(entity[attribute]) == list:
            for index, new_entity in enumerate(entity[attribute]):
                if type(new_entity) == dict:
                    entity[attribute][index] = replace_absolute_references_in_entity_with_alias(
                        new_entity, dependencies
                    )
    return entity
