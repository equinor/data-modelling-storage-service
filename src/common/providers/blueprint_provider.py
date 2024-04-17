import uuid
from collections.abc import Callable
from functools import lru_cache

from authentication.models import User
from common.address import Address
from common.exceptions import NotFoundException
from common.providers.address_resolver.address_resolver import (
    ResolvedAddress,
    resolve_address,
)
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from storage.data_source_interface import DataSource
from storage.internal.data_source_repository import get_data_source


def substitute_get_blueprint(*args, **kwargs):
    raise ValueError("'get_blueprint' should not be called when fetching blueprints")


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

    @lru_cache(maxsize=128)  # noqa B019
    def get_data_source_cached(self, data_source_id: str, user: User) -> DataSource:
        # BlueprintProvider needs its own  'get_data_source' function to avoid circular imports
        return self.get_data_source(data_source_id, self.user, substitute_get_blueprint)

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)  # noqa: B019
    def get_blueprint_with_extended_attributes(self, type: str) -> Blueprint:
        blueprint: Blueprint = self.get_blueprint(type)
        blueprint.realize_extends(self.get_blueprint)
        return blueprint

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)  # noqa: B019
    def get_blueprint(self, type: str) -> Blueprint:
        logger.debug(f"Cache miss! Fetching blueprint '{type}' '{hash(self)}'")
        try:
            resolved_address: ResolvedAddress = self.resolve_address(
                Address.from_absolute(type),
                lambda data_source_name: self.get_data_source_cached(data_source_name, self.user),
            )
        except NotFoundException as ex:
            raise NotFoundException(
                f"Blueprint referenced with '{type}' could not be found. Make sure the reference is correct.",
                data=ex.dict(),
            ) from ex
        resolved_address = self.resolve_address(
            Address.from_relative(
                resolved_address.entity["address"],
                resolved_address.document_id,
                resolved_address.data_source_id,
            ),
            lambda data_source_name: self.get_data_source_cached(data_source_name, self.user),
        )
        return Blueprint(resolved_address.entity, type)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
            self.get_blueprint_with_extended_attributes.cache_clear()
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


default_blueprint_provider = get_blueprint_provider()
