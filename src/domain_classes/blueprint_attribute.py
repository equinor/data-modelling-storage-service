from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    model_validator,
)

from domain_classes.dimension import Dimension
from enums import PRIMITIVES, SIMOS


class BlueprintAttribute(BaseModel):
    name: str
    attribute_type: str = Field(..., alias="attributeType")
    type: str = SIMOS.BLUEPRINT_ATTRIBUTE.value
    description: str = ""
    label: str = ""
    default: StrictStr | StrictInt | StrictFloat | StrictBool | list | dict | None = None
    dimensions: Dimension | None = None
    ensure_uid: bool = Field(False, alias="ensureUID")
    optional: bool = False
    contained: bool = True
    enum_type: str = Field("", alias="enumType")

    def to_dict(self, by_alias: bool = True):
        return {
            **self.dict(by_alias=by_alias),
            "dimensions": self.dimensions.to_dict() if self.dimensions else None,
        }

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    @model_validator(mode="before")
    def deserialize_dimensions(self):
        self["dimensions"] = Dimension(
            self.get("dimensions") or "", self.get("attributeType", self.get("attribute_type"))
        )
        return self

    def __repr__(self):
        return (
            f"Name: '{self.name}', Type: '{self.attribute_type}' "
            f"Contained: '{self.contained}', Optional: '{self.optional}'"
        )

    @property
    def is_array(self):
        if not self.dimensions:
            return False
        return self.dimensions.is_array()

    @property
    def is_matrix(self):
        if not self.dimensions:
            return False
        return self.dimensions.is_matrix()

    @property
    def is_primitive(self):
        return self.attribute_type in PRIMITIVES

    @property
    def is_optional(self):
        # todo get default from blueprint attribute optional's default value.
        default_optional = False
        return self.optional if self.optional is not None else default_optional
