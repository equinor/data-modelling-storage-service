from collections import defaultdict

from pydantic import BaseModel, Field

from domain_classes.storage_recipe import StorageRecipe
from domain_classes.ui_recipe import Recipe


class Lookup(BaseModel):
    # TODO: When openapi-generator supports OpenAPI v3.1, replace dict[str.. -> dict[common_type_constrained_string
    ui_recipes: dict[str, list[Recipe]] = Field(default_factory=lambda: defaultdict(list), alias="uiRecipes")
    storage_recipes: dict[str, list[StorageRecipe]] = Field(
        default_factory=lambda: defaultdict(list), alias="storageRecipes"
    )
