from pydantic import BaseModel

from authentication.models import User
from common.utils.get_storage_recipe import (
    default_form_edit,
    default_initial_ui_recipe,
    default_list_recipe,
    default_yaml_view,
)
from domain_classes.lookup import Lookup
from restful.request_types.shared import TypeConstrainedString
from services.document_service import DocumentService
from storage.internal.lookup_tables import get_lookup


class GetBlueprintResponse(BaseModel):
    blueprint: dict
    uiRecipes: list[dict]
    storageRecipes: list[dict]


default_ui_recipes = [default_form_edit, default_yaml_view, default_list_recipe]


def get_blueprint_use_case(type: TypeConstrainedString, context: str | None, user: User) -> dict:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(type)

    if not context:
        return {
            "blueprint": blueprint.to_dict(),
            "uiRecipes": [ur.dict(by_alias=True) for ur in default_ui_recipes],
            # TODO: Generate default storage recipe
            "storageRecipes": [],
        }

    lookup: Lookup = get_lookup(context)
    # Get type specific recipes
    ui_recipes: list = lookup.ui_recipes.get(type, [])

    # If no recipe link exists for the type, use the contexts default. If none, use builtin default
    if not ui_recipes:
        ui_recipes = lookup.ui_recipes.get("_default_", default_ui_recipes)

    # No UiRecipe with dimensions "*" found. Add default list recipe
    if not next((ur for ur in ui_recipes if ur.dimensions == "*"), None):
        ui_recipes.append(default_list_recipe)

    storage_recipes = lookup.storage_recipes.get(type, [])
    if not storage_recipes:
        storage_recipes = lookup.storage_recipes.get("_default_", [])

    return {
        "blueprint": blueprint.to_dict(),
        "initialUiRecipe": lookup.initial_ui_recipes[type].dict()
        if lookup.initial_ui_recipes.get(type)
        else default_initial_ui_recipe.dict(by_alias=True),
        "uiRecipes": [ur.dict(by_alias=True) for ur in ui_recipes],
        "storageRecipes": [sr.dict(by_alias=True) for sr in storage_recipes],
    }
