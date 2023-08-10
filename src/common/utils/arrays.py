from typing import Any, Callable, Type

from domain_classes.dimension import Dimension


def create_default_array(
    dimension: Dimension,
    blueprint_provider: Callable,
    create_entity_class: Type[
        Any
    ],  # TODO use Type[CreateEntity]. can't use it now due to circular import. Needs refactoring.
    default_array_value: list[Any] = None,
) -> list:
    """
    Create an array with default values with a given dimension.

    - Dimension.dimensions = ["2,1"] represents a 2 dimensional array where inner arrays have length one - for example [[1], [3]]
    - Dimension.dimensions = ["*"] represents a one dimensional array of any length.

    Hard coded default values for different types (type is specified in the Dimension class):
    - integer: 0
    - number: 0.00
    - boolean: False
    - string: ""

    For complex types (For example dmss://system/SIMOS/Package), default value is found from the 'create_entity_class'.

    For dimension ["*"], default_array_value can be used to create an array with a given default value.
    """
    dimensions = dimension.dimensions
    if dimensions == [""]:
        raise Exception("This attribute is not an array!")
    if len(dimensions) == 1:
        if dimensions[0] == "*":
            return default_array_value if default_array_value is not None else []

        # TODO use default value from blueprint if it exists for cases other than dimensions[0] == "*"
        # Return a list initialized with default values for the size of the array.
        if dimension.type is int:
            return [0 for n in range(int(dimensions[0]))]
        if dimension.type is float:
            return [0.00 for n in range(int(dimensions[0]))]
        if dimension.type is str:
            return ["" for n in range(int(dimensions[0]))]
        if dimension.type is bool:
            return [False for n in range(int(dimensions[0]))]
        else:
            # For fixed complex types, create the entity with default values. Set name from list index.
            return [create_entity_class(blueprint_provider, dimension.type).entity for n in range(int(dimensions[0]))]

    if dimensions[0] == "*":
        # If the size of the rank is "*" we only create one nested list.
        nested_list = [
            create_default_array(
                Dimension(remove_first_and_join(dimensions), dimension.type),
                blueprint_provider,
                create_entity_class,
                default_array_value,
            )
        ]
    else:
        # If the size of the rank in NOT "*", we expect an Integer, and create n number of nested lists.
        nested_list = [
            create_default_array(
                Dimension(remove_first_and_join(dimensions), dimension.type),
                blueprint_provider,
                create_entity_class,
                default_array_value,
            )
            for n in range(int(dimensions[0]))
        ]
    return nested_list


def remove_first_and_join(input_list: list[str]) -> str:
    """
    Remove the first element of the list and convert to a string equivalent.
    Examples:
    ["1","2","3","4"] -> "2,3,4"
    ["0","0"] -> "0"
    ["4"] -> ""
    [""] -> ""
    """
    if len(input_list) == 1:
        return ""
    if len(input_list) <= 1:
        return ",".join(input_list)
    else:
        return ",".join(input_list[1:])
