from enum import Enum
from typing import List

from pydantic import BaseModel

from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import PRIMITIVES


class RecipePlugin(Enum):
    INDEX = "INDEX"
    DEFAULT = "DEFAULT"


class RecipeAttribute(BaseModel):
    name: str
    contained: bool = True
    field: str = None
    array_field: str = None
    collapsible: bool = None
    ui_recipe: str = None
    mapping: str = None


class Recipe(BaseModel):
    name: str
    attributes: List[RecipeAttribute] = []
    description: str = ""
    plugin: str = "Default"
    category: str = ""
    config: dict = None
    label: str = ""

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
            if attribute.is_array():
                return array_contained
            else:
                return single_contained


class DefaultRecipe(Recipe):
    def __init__(self, attributes: List[BlueprintAttribute]):
        recipe_attributes = [RecipeAttribute(name=attr.name, contained=True) for attr in attributes]
        super().__init__("Default", attributes=recipe_attributes)
