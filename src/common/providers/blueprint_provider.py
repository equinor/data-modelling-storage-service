from functools import lru_cache

from authentication.models import User
from common.address import Address
from common.providers.address_resolver import ResolvedAddress, resolve_address
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from storage.internal.data_source_repository import get_data_source


class BlueprintProvider:
    def __init__(self, user: User):
        self.user = user

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        logger.debug(f"Cache miss! Fetching blueprint '{type}'")
        resolved_address: ResolvedAddress = resolve_address(
            Address.from_absolute(type), lambda data_source_name: get_data_source(data_source_name, self.user)
        )
        resolved_address = resolve_address(
            Address.from_relative(
                resolved_address.entity["address"], resolved_address.document_id, resolved_address.data_source_id
            ),
            lambda data_source_name: get_data_source(data_source_name, self.user),
        )
        return Blueprint(resolved_address.entity, type)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_blueprint_provider(user):
    return BlueprintProvider(user)
