from functools import lru_cache

from authentication.models import User
from common.address import Address
from common.utils.logging import logger
from common.utils.resolve_reference import ResolvedReference, resolve_reference
from config import config
from domain_classes.blueprint import Blueprint
from storage.internal.data_source_repository import get_data_source


class BlueprintProvider:
    def __init__(self, user: User):
        self.user = user

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        logger.debug(f"Cache miss! Fetching blueprint '{type}'")
        resolved_reference: ResolvedReference = resolve_reference(
            Address.fromabsolute(type), lambda data_source_name: get_data_source(data_source_name, self.user)
        )
        resolved_reference = resolve_reference(
            Address.fromrelative(
                resolved_reference.entity["address"], resolved_reference.document_id, resolved_reference.data_source_id
            ),
            lambda data_source_name: get_data_source(data_source_name, self.user),
        )
        return Blueprint(resolved_reference.entity, type)

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_blueprint_provider(user):
    return BlueprintProvider(user)
