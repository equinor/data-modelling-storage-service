# Convert dmt attribute_types to python types. If complex, return type as string.
from typing import Any

from enums import BuiltinDataTypes


def _get_data_type_from_dmt_type(
    attribute_type: str,
) -> type[bool] | type[int] | type[float] | type[str] | str:
    try:
        type_enum = BuiltinDataTypes(attribute_type)
        return type_enum.to_py_type()
    except ValueError:
        return attribute_type


class Dimension:
    def __init__(self, dimensions: str, attribute_type: str):
        """
        dimensions: define the structure of the array. For example:
        - "*" is a one dimensional array of any length.
        - "*,*" is a two dimensional array of any length.
        - "2,1" is a 2 dimensional array where inner arrays have length one - for example [[1], [3]]

        attribute_type: define what type the values in the array have. Primitive types: boolean, integer, string and number)
        are converted to python types. For complex types, for example "dmss://system/SIMOS/Package",
        a string value is stored.
        """
        self.dimensions: list[str] = dimensions.split(",")
        self.type: type[bool] | type[int] | type[float] | type[str] | str | Any = _get_data_type_from_dmt_type(
            attribute_type
        )
        self.value = None

    def is_array(self) -> bool:
        return self.dimensions != [""]

    # TODO remove function - it is never used for anything useful
    def is_matrix(self) -> bool:
        return len(self.dimensions) > 1

    # TODO remove function - it is never used for anything useful
    # If the inner most dimension is "*", the Dimension is unfixed
    def is_unfixed(self) -> bool:
        return self.dimensions[-1] == "*"

    def to_dict(self) -> str:
        return ",".join(self.dimensions)
