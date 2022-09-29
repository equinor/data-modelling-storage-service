from typing import Union

from pydantic import BaseModel, Field, validator

from domain_classes.dimension import Dimension
from enums import PRIMITIVES, SIMOS


class BlueprintAttribute(BaseModel):
    name: str
    attribute_type: str = Field(..., alias="attributeType")
    type: str = SIMOS.BLUEPRINT_ATTRIBUTE.value
    description: str = ""
    label: str = ""
    default: Union[str, list] = ""
    dimensions: Dimension = None
    optional: bool = False
    contained: bool = True
    enum_type: str = Field("", alias="enumType")

    def to_dict(self, by_alias: bool = True):
        return {**self.dict(by_alias=by_alias), "dimensions": self.dimensions.to_dict()}

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    @validator("dimensions", pre=True, always=True)
    def deserialize_dimensions(cls, value, values):
        return Dimension(value or "", values["attribute_type"])

    def __repr__(self):
        return (
            f"Name: '{self.name}', Type: '{self.attribute_type}' "
            f"Contained: '{self.contained}', Optional: '{self.optional}'"
        )

    @property
    def is_array(self):
        return self.dimensions.is_array()

    @property
    def is_matrix(self):
        return self.dimensions.is_matrix()

    @property
    def is_primitive(self):
        return self.attribute_type in PRIMITIVES

    @property
    def is_optional(self):
        # todo get default from blueprint attribute optional's default value.
        default_optional = False
        return self.optional if self.optional is not None else default_optional
