from domain_classes.dependency import Dependency


def is_alias(path: str, dependencies: list[Dependency]):
    NUM_SPLITS = 1
    path_start = path.split(":", NUM_SPLITS)[0]
    for dependency in dependencies:
        if path_start == dependency.alias:
            return True
    return False


def replace_absolute_references_with_alias(entity: dict, dependencies: list[Dependency]):
    """Replace path in an entity with alias defined in a list of dependencies.

    (for example, replace "dmss://system/SIMOS/Package" with "CORE:Package".)
    """
    attribute_to_update = ("type", "attributeType", "extends", "_blueprintPath_")  # These keys may contain a reference
    for attribute in entity:
        if attribute == "attributes" or attribute == "content":
            # "attributes" and "content" contain list of entities.
            for new_entity in entity[attribute]:
                replace_absolute_references_with_alias(new_entity, dependencies)
        elif attribute in attribute_to_update:
            for dependency in dependencies:
                if attribute == "extends":
                    # "extends" attribute contains a list of absolute references. Each list item is treated separately.
                    for index, absolute_reference in enumerate(entity[attribute]):
                        if not is_alias(entity[attribute][index], dependencies):
                            path_after_alias = absolute_reference.split(dependency.get_absolute_reference())[-1]
                            entity[attribute][index] = f"{dependency.alias}:{path_after_alias}"
                            break
                elif entity[attribute].startswith(dependency.get_absolute_reference()):
                    path_after_alias = entity[attribute].split(dependency.get_absolute_reference())[-1]
                    entity[attribute] = f"{dependency.alias}:{path_after_alias}"
                    break
