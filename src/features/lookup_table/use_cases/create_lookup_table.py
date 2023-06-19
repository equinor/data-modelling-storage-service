from authentication.access_control import DEFAULT_ACL, access_control
from authentication.models import AccessLevel, User
from common.reference import Reference
from domain_classes.lookup import Lookup
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from domain_classes.ui_recipe import Recipe
from enums import SIMOS, StorageDataTypes
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from storage.internal.lookup_tables import get_lookup, insert_lookup


def create_lookup_table_use_case(
    recipe_package_paths: list[str], name: str, user: User, repository_provider=get_data_source
) -> None:
    """
    Create lookup table. If the lookup table already exist, the lookup table will be updated.
    """
    access_control(DEFAULT_ACL, AccessLevel.WRITE, user)

    document_service = DocumentService(repository_provider=repository_provider, user=user)
    lookup_class_attributes = list(Lookup.__annotations__.keys())
    combined_lookup = Lookup().dict()
    for path in recipe_package_paths:
        recipe_package = document_service.get_document(
            Reference(*path.split("/", 1)[::-1]), depth=999, resolve_links=True
        )

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
        for attribute in lookup_class_attributes:
            combined_lookup[attribute].update(lookup_as_dict[attribute])

    insert_lookup(name, combined_lookup)

    document_service.get_storage_recipes.cache_clear()
    get_lookup.cache_clear()
