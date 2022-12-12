from authentication.models import User
from domain_classes.lookup import Lookup
from restful.request_types.shared import common_type_constrained_string
from services.document_service import DocumentService
from storage.internal.lookup_tables import get_lookup


def get_blueprint_use_case(type: common_type_constrained_string, context: str, user: User) -> dict:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(type)
    lookup: Lookup = get_lookup(context)
    ui_recipes = lookup.ui_recipes.get(type, [])
    storage_recipes = lookup.storage_recipes.get(type, [])

    return {
        "blueprint": blueprint.to_dict(),
        "uiRecipes": [ur.dict(by_alias=True) for ur in ui_recipes],
        "storageRecipes": [sr.dict(by_alias=True) for sr in storage_recipes],
    }
