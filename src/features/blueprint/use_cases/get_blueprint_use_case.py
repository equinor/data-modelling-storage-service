from pydantic import BaseModel

from authentication.models import User
from domain_classes.lookup import Lookup
from enums import SIMOS
from restful.request_types.shared import common_type_constrained_string
from services.document_service import DocumentService
from storage.internal.lookup_tables import get_lookup

default_ui_recipes = [
    {
        "name": "Yaml",
        "type": SIMOS.UI_RECIPE.value,
        "plugin": "yaml-view",
        "roles": ["dmss-admin"],
        "category": "view",
    },
    {"name": "Edit", "type": SIMOS.UI_RECIPE.value, "plugin": "form", "category": "edit"},
]

default_storage_recipes: list[dict] = []


class GetBlueprintResponse(BaseModel):
    blueprint: dict
    uiRecipes: list[dict]
    storageRecipes: list[dict]


def get_blueprint_use_case(type: common_type_constrained_string, context: str | None, user: User) -> dict:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(type)

    if not context:
        return {
            "blueprint": blueprint.to_dict(),
            "uiRecipes": default_ui_recipes,
            "storageRecipes": default_storage_recipes,
        }

    lookup: Lookup = get_lookup(context)
    # Get type specific recipes
    ui_recipes = lookup.ui_recipes.get(type, [])

    # If no recipe link exists for the type, use the contexts default
    if not ui_recipes:
        ui_recipes = lookup.ui_recipes.get("_default_", [])

    storage_recipes = lookup.storage_recipes.get(type, [])
    if not storage_recipes:
        storage_recipes = lookup.storage_recipes.get("_default_", [])

    return {
        "blueprint": blueprint.to_dict(),
        "uiRecipes": [ur.dict(by_alias=True) for ur in ui_recipes],
        "storageRecipes": [sr.dict(by_alias=True) for sr in storage_recipes],
    }
