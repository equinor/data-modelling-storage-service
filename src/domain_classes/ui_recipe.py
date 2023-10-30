from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import PRIMITIVES, SIMOS


class RecipePlugin(Enum):
    INDEX = "INDEX"
    DEFAULT = "DEFAULT"


class RecipeAttribute(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str = SIMOS.UI_ATTRIBUTE.value
    attribute_type: str | None = Field(None, alias="attributeType")
    label: str | None = None
    contained: bool = True
    field: str | None = None
    array_field: str | None = None
    collapsible: bool | None = None
    ui_recipe: str | None = None
    mapping: str | None = None


class Recipe(BaseModel):
    name: str
    type: str = SIMOS.UI_RECIPE.value
    attributes: list[RecipeAttribute] = []
    description: str = ""
    plugin: str = "Default"
    category: str = ""
    roles: list[str] | None = None
    config: dict | None = None
    label: str = ""
    dimensions: str = ""

    def get_attribute_by_name(self, key):
        return next((attr for attr in self.attributes if attr.name == key), None)

    def is_contained(self, attribute: BlueprintAttribute, plugin: RecipePlugin = RecipePlugin.DEFAULT):
        if plugin == RecipePlugin.INDEX:
            primitive_contained = False
            array_contained = True
            single_contained = True
        else:
            primitive_contained = True
            array_contained = False
            single_contained = False

        ui_attribute = self.get_attribute_by_name(attribute.name)
        if ui_attribute:
            return ui_attribute.contained

        if attribute.attribute_type in PRIMITIVES:
            return primitive_contained
        else:
            if attribute.is_array:
                return array_contained
            else:
                return single_contained
