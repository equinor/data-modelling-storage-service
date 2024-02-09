import uuid
from collections.abc import Callable
from functools import lru_cache

from authentication.models import User
from common.providers.address_resolver.address_resolver import (
    resolve_address,
)
from common.providers.cached_blueprint_provider import (
    cached_get_blueprint,
    cached_get_blueprint_with_extended_attributes,
)
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from storage.internal.data_source_repository import get_data_source


class BlueprintProvider:
    def __init__(
        self,
        user: User,
        get_data_source: Callable = get_data_source,
        resolve_address: Callable = resolve_address,
    ):
        self.user = user
        self.get_data_source = get_data_source
        self.resolve_address = resolve_address
        self.id = uuid.uuid4()

    def get_blueprint_with_extended_attributes(self, type: str) -> Blueprint:
        return cached_get_blueprint_with_extended_attributes(
            type, self.get_data_source, self.resolve_address, self.user
        )

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)  # noqa: B019
    def get_blueprint(self, type: str) -> Blueprint:
        return cached_get_blueprint(type, self.get_data_source, self.resolve_address, self.user)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            cached_get_blueprint_with_extended_attributes.cache_clear()
            cached_get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)


def get_blueprint_provider():
    # TODO: Hard coding the admin user here is a short term performance hack.
    # This hack leads to any authenticated user can read any document if it's accessed as a blueprint
    # The proper fix would be to either "compile" all blueprint at startup, or implement a repository/access control
    # system that lends itself to cache better than what we have now (6.2.2024)
    logger.debug("Cache miss! Creating new blueprint provider!")
    return BlueprintProvider(
        User(**{"user_id": config.DMSS_ADMIN, "email": "mock_dmss_admin@example.com", "full_name": "Mock admin user"})
    )
