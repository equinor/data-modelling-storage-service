from common.exceptions import NotFoundException
from domain_classes.lookup import Lookup
from domain_classes.storage_recipe import StorageRecipe
from domain_classes.ui_recipe import Recipe
from enums import SIMOS, StorageDataTypes
from storage.internal.lookup_tables import get_lookup

default_yaml_view = Recipe(
    **{
        "name": "Yaml",
        "type": SIMOS.UI_RECIPE.value,
        "repository_plugins": "@development-framework/dm-core-plugins/yaml",
    }
)
default_form_edit = Recipe(
    **{
        "name": "Edit",
        "type": SIMOS.UI_RECIPE.value,
        "repository_plugins": "@development-framework/dm-core-plugins/form",
    }
)
default_list_recipe = Recipe(
    **{
        "name": "List",
        "type": SIMOS.UI_RECIPE.value,
        "repository_plugins": "@development-framework/dm-core-plugins/list",
        "dimensions": "*",
    }
)

default_initial_ui_recipe = Recipe(
    **{
        "name": "RecipeSelect",
        "type": SIMOS.UI_RECIPE.value,
        "repository_plugins": "@development-framework/dm-core-plugins/view_selector/tabs",
        "config": {
            "type": "dmss://system/Plugins/dm-core-plugins/view_selector/ViewSelectorConfig",
            "items": [
                {
                    "type": "dmss://system/Plugins/dm-core-plugins/view_selector/ViewSelectorItem",
                    "label": "Yaml",
                    "viewConfig": {
                        "type": "dmss://system/SIMOS/InlineRecipeViewConfig",
                        "recipe": {
                            "type": "dmss://system/SIMOS/UiRecipe",
                            "name": "YAML",
                            "description": "YAML representation",
                            "repository_plugins": "@development-framework/dm-core-plugins/yaml",
                        },
                        "scope": "self",
                        "eds_icon": "code",
                    },
                },
                {
                    "type": "dmss://system/Plugins/dm-core-plugins/view_selector/ViewSelectorItem",
                    "label": "Edit",
                    "viewConfig": {
                        "type": "dmss://system/SIMOS/InlineRecipeViewConfig",
                        "recipe": {
                            "type": "dmss://system/SIMOS/UiRecipe",
                            "name": "Edit",
                            "description": "Default edit",
                            "repository_plugins": "@development-framework/dm-core-plugins/form",
                        },
                        "scope": "self",
                        "eds_icon": "edit",
                    },
                },
            ],
        },
    }
)


def storage_recipe_provider(type: str, context: str | None = None) -> list[StorageRecipe]:
    if not context:
        return []

    try:
        lookup: Lookup = get_lookup(context)
    except NotFoundException as error:
        if context == "DMSS":
            return []
        raise error
    # Get type specific recipes
    storage_recipes = lookup.storage_recipes.get(type, [])
    # If no recipe link exists for the type, use the contexts default
    if not storage_recipes:
        storage_recipes = lookup.storage_recipes.get("_default_", [])

    return storage_recipes


def create_default_storage_recipe() -> list[StorageRecipe]:
    return [
        StorageRecipe(
            name="Default",
            storage_affinity=StorageDataTypes.DEFAULT,
            attributes={},
        )
    ]
