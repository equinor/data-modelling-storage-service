from authentication.access_control import DEFAULT_ACL, access_control
from authentication.models import AccessLevel, User
from domain_classes.lookup import Lookup
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from domain_classes.ui_recipe import Recipe
from enums import SIMOS, StorageDataTypes
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from storage.internal.lookup_tables import insert_lookup


def create_lookup_table_use_case(
    recipe_package_path: str, name: str, user: User, repository_provider=get_data_source
) -> None:
    access_control(DEFAULT_ACL, AccessLevel.WRITE, user)

    document_service = DocumentService(repository_provider=repository_provider, user=user)

    recipe_package = document_service.get_by_path(recipe_package_path)

    lookup: Lookup = Lookup()

    for node in recipe_package.traverse():
        if node.type == SIMOS.RECIPE_LINK.value:
            ui_recipes = [Recipe(**r) for r in node.entity.get("uiRecipes", [])]

            storage_recipes = [
                StorageRecipe(
                    name=r["name"],
                    storage_affinity=r.get("storageAffinity", StorageDataTypes.DEFAULT),
                    attributes={attribute["name"]: StorageAttribute(**attribute) for attribute in r["attributes"]},
                )
                for r in node.entity.get("storageRecipes", [])
            ]

            lookup.storage_recipes[node.entity["_blueprintPath_"]].extend(storage_recipes)
            lookup.ui_recipes[node.entity["_blueprintPath_"]].extend(ui_recipes)

    insert_lookup(name, lookup.dict())
