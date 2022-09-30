from typing import Callable, Dict, List

from pydantic import ValidationError

from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import DefaultStorageRecipe, StorageRecipe
from domain_classes.ui_recipe import DefaultRecipe, Recipe
from enums import PRIMITIVES, StorageDataTypes


def get_storage_recipes(recipes: List[Dict], attributes: List[BlueprintAttribute]):
    if not recipes:
        return [DefaultStorageRecipe(attributes)]
    else:
        return [
            StorageRecipe(
                name=recipe["name"],
                storageAffinity=recipe.get("storageAffinity", StorageDataTypes.DEFAULT.value),
                attributes=recipe["attributes"],
            )
            for recipe in recipes
        ]


class Blueprint:
    def __init__(self, entity: dict):
        self.name = entity["name"]
        self.description = entity.get("description", "")
        self.abstract = entity.get("abstract", False)
        self.extends = entity.get("extends", [])
        self.type = entity["type"]
        self.entity = entity
        self.attributes: List[BlueprintAttribute] = [
            BlueprintAttribute(**attribute) for attribute in entity.get("attributes", [])
        ]
        self.storage_recipes: List[StorageRecipe] = get_storage_recipes(
            entity.get("storageRecipes", []), self.attributes
        )
        try:
            self.ui_recipes: List[Recipe] = [Recipe(**recipe_dict) for recipe_dict in entity.get("uiRecipes", [])]
        except ValidationError as e:
            print(e)

    @classmethod
    def from_dict(cls, adict):
        instance = cls(adict)
        instance.attributes = [BlueprintAttribute(**attr) for attr in adict.get("attributes", [])]
        instance.storage_recipes = get_storage_recipes(adict.get("storageRecipes", []), instance.attributes)
        instance.ui_recipes = [Recipe.from_dict(recipe_dict) for recipe_dict in adict.get("uiRecipes", [])]
        return instance

    def get_required_attributes(self):
        return [attribute for attribute in self.attributes if attribute.optional is False]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "abstract": self.abstract,
            "extends": self.extends,
            "attributes": [attribute.to_dict() for attribute in self.attributes],
            "storageRecipes": [recipe.to_dict() for recipe in self.storage_recipes],
            "uiRecipes": [recipe.dict() for recipe in self.ui_recipes],
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __str__(self):
        return (
            f"Name: '{self.name}', Attributes: "
            f"{[f'{n}({self.get_attribute_type_by_key(n)})' for n in self.get_attribute_names()]}"
        )

    def get_none_primitive_types(self) -> List[BlueprintAttribute]:
        blueprints = [attribute for attribute in self.attributes if attribute.attribute_type not in PRIMITIVES]
        return blueprints

    def get_primitive_types(self) -> List[BlueprintAttribute]:
        # TODO function does not return the primitive types from the blueprint that self extends from (self.extends)
        blueprints = [attribute for attribute in self.attributes if attribute.attribute_type in PRIMITIVES]
        return blueprints

    def get_attribute_names(self) -> List[str]:
        return [attribute.name for attribute in self.attributes]

    def get_ui_recipe(self, name=None):
        found = next((x for x in self.ui_recipes if x.name == name), None)
        if found:
            return found
        else:
            return DefaultRecipe(attributes=[attribute for attribute in self.attributes])

    def get_ui_recipe_by_plugin(self, name=None):
        found = next((x for x in self.ui_recipes if x.plugin == name), None)
        if found:
            return found
        else:
            return DefaultRecipe(attributes=[attribute for attribute in self.attributes])

    def get_attribute_type_by_key(self, key):
        return next((attr.attribute_type for attr in self.attributes if attr.name == key), None)

    def get_attribute_by_name(self, key) -> BlueprintAttribute:
        return next((attr for attr in self.attributes if attr.name == key), None)

    def get_model_contained_by_name(self, key):
        return next((attr.contained for attr in self.attributes if attr.name == key), True)

    def is_attr_removable(self, attribute_name):
        for attr in self.attributes:
            if attr.name == attribute_name and not attr.is_primitive:
                if attr.is_array:
                    return False
                elif not attr.is_optional:
                    return False
        return True

    def realize_extends(self, blueprint_provider: Callable[[str], "Blueprint"]):
        """
        Recursive
        Inherits attributes, storage-, and ui-recipies from "extended" blueprints
        Overrides attributes with similar names from ancestor blueprints, except from DefaultStorageRecipe
        """
        new_attributes: Dict[str, BlueprintAttribute] = {}
        new_storage_recipes: Dict[str, StorageRecipe] = {}
        new_ui_recipes: Dict[str, Recipe] = {}

        for base in self.extends:
            base_blueprint: Blueprint = blueprint_provider(base)
            base_blueprint.realize_extends(blueprint_provider)
            # Overrides left. attribute names are CASE-INSENSITIVE
            # DefaultStorageRecipes does not override recipes from base
            new_attributes.update({attr.name.lower(): attr for attr in base_blueprint.attributes})
            new_storage_recipes.update(
                {
                    attr.name.lower(): attr
                    for attr in base_blueprint.storage_recipes
                    if not isinstance(attr, DefaultStorageRecipe)
                }
            )
            new_ui_recipes.update({attr.name.lower(): attr for attr in base_blueprint.ui_recipes})

        new_attributes.update({attr.name.lower(): attr for attr in self.attributes})
        new_storage_recipes.update(
            {attr.name.lower(): attr for attr in self.storage_recipes if not isinstance(attr, DefaultStorageRecipe)}
        )
        new_ui_recipes.update({attr.name.lower(): attr for attr in self.ui_recipes})

        self.attributes = [attr for attr in new_attributes.values()]
        # Make sure storage_recipes are not empty (use DefaultStorageRecipe)
        self.storage_recipes = (
            [attr for attr in new_storage_recipes.values()] if new_storage_recipes else self.storage_recipes
        )
        self.ui_recipes = [attr for attr in new_ui_recipes.values()]
