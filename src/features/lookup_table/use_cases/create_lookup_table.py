from authentication.access_control import assert_user_has_access
from authentication.models import AccessControlList, AccessLevel, User
from common.address import Address
from domain_classes.lookup import Lookup
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from domain_classes.ui_recipe import Recipe
from enums import SIMOS, StorageDataTypes
from services.document_service.document_service import DocumentService
from storage.internal.lookup_tables import get_lookup, insert_lookup


def create_lookup_table_use_case(
    recipe_package_paths: list[str],
    name: str,
    user: User,
) -> None:
    """
    Create lookup table. If the lookup table already exist, the lookup table will be updated.
    """
    assert_user_has_access(AccessControlList.default(), AccessLevel.WRITE, user)

    document_service = DocumentService(user=user)
    combined_lookup = Lookup().dict()
    for path in recipe_package_paths:
        recipe_package = document_service.get_document(Address(*path.split("/", 1)[::-1]), depth=999)

        lookup: Lookup = Lookup()

        recipes_to_extend: dict[str, list[str]] = {}

        for node in recipe_package.traverse():
            if node.type == SIMOS.RECIPE_LINK.value:
                blueprint_path = node.entity["_blueprintPath_"]

                # Check if blueprint exists. If not, exception is raised
                if blueprint_path != "_default_":
                    document_service.get_blueprint(blueprint_path)

                ui_recipes = [Recipe(**r) for r in node.entity.get("uiRecipes", [])]
                initial_ui_recipe = (
                    Recipe(**node.entity["initialUiRecipe"]) if node.entity.get("initialUiRecipe") else None
                )

                storage_recipes = [
                    StorageRecipe(
                        name=r["name"],
                        storage_affinity=r.get("storageAffinity", StorageDataTypes.DEFAULT),
                        attributes={attribute["name"]: StorageAttribute(**attribute) for attribute in r["attributes"]},
                    )
                    for r in node.entity.get("storageRecipes", [])
                ]

                if extends := node.entity.get("extends"):
                    recipes_to_extend[blueprint_path] = extends

                lookup.storage_recipes[blueprint_path].extend(storage_recipes)
                lookup.ui_recipes[blueprint_path].extend(ui_recipes)
                lookup.initial_ui_recipes[blueprint_path] = initial_ui_recipe

        lookup.extends = recipes_to_extend
        lookup.realize_extends()

        lookup_as_dict = lookup.dict()
        for attribute in ["ui_recipes", "storage_recipes", "initial_ui_recipes", "extends"]:
            combined_lookup[attribute].update(lookup_as_dict[attribute])

    combined_lookup["paths"] = recipe_package_paths
    insert_lookup(name, combined_lookup)

    get_lookup.cache_clear()
