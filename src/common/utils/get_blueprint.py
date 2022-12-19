from functools import lru_cache

from authentication.models import User
from common.exceptions import NotFoundException
from common.utils.get_document_by_path import get_document_by_absolute_path
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from domain_classes.lookup import Lookup
from domain_classes.storage_recipe import StorageRecipe
from enums import SIMOS
from storage.internal.lookup_tables import get_lookup


class BlueprintProvider:
    def __init__(self, user: User):
        self.user = user

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        logger.debug(f"Cache miss! Fetching blueprint '{type}'")
        document: dict = get_document_by_absolute_path(type, self.user)
        return Blueprint(document)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_blueprint_provider(user):
    return BlueprintProvider(user)


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
