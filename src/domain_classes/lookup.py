from collections import defaultdict
from typing import Tuple

from pydantic import BaseModel, Field

from domain_classes.storage_recipe import StorageRecipe
from domain_classes.ui_recipe import Recipe


def resolve_extended_recipe_links_recursive(
    blueprint_path: str, lookup: "Lookup", extends: dict[str, list[str]]
) -> Tuple[list[StorageRecipe], list[Recipe]]:
    if not extends.get(blueprint_path):  # It does not extend anything, just return its own recipes
        return lookup.storage_recipes[blueprint_path], lookup.ui_recipes[blueprint_path]

    inherited_ui_recipes: list[Recipe] = []
    inherited_storage_recipes: list[StorageRecipe] = []
    for type in extends[blueprint_path]:
        new_storage_recipe, new_ui_recipes = resolve_extended_recipe_links_recursive(type, lookup, extends)
        inherited_ui_recipes = inherited_ui_recipes + new_ui_recipes
        inherited_storage_recipes = inherited_storage_recipes + new_storage_recipe

    own_and_inherited_ui = lookup.ui_recipes[blueprint_path] + inherited_ui_recipes
    own_and_inherited_storage = lookup.storage_recipes[blueprint_path] + inherited_storage_recipes
    return own_and_inherited_storage, own_and_inherited_ui


class Lookup(BaseModel):
    # TODO: When openapi-generator supports OpenAPI v3.1, replace dict[str,.. -> dict[common_type_constrained_string,...
    ui_recipes: dict[str, list[Recipe]] = Field(default_factory=lambda: defaultdict(list), alias="uiRecipes")
    storage_recipes: dict[str, list[StorageRecipe]] = Field(
        default_factory=lambda: defaultdict(list), alias="storageRecipes"
    )
    initial_ui_recipes: dict[str, Recipe | None] = Field(default_factory=lambda: {}, alias="initialUiRecipes")
    extends: dict[str, list[str]] = {}

    def realize_extends(self):
        new_ui_recipes = {}
        new_storage_recipes = {}

        for blueprint_path in self.extends:
            resolved_storage, resolved_ui = resolve_extended_recipe_links_recursive(blueprint_path, self, self.extends)
            new_ui_recipes[blueprint_path] = resolved_ui
            new_storage_recipes[blueprint_path] = resolved_storage

        self.ui_recipes.update(new_ui_recipes)
        self.storage_recipes.update(new_storage_recipes)

    class Config:
        allow_population_by_field_name = True
