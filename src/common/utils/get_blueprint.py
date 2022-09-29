from functools import lru_cache

from authentication.models import User
from common.exceptions import NotFoundException
from common.utils.get_document_by_path import get_document_by_ref
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint


class BlueprintProvider:
    def __init__(self, user: User):
        self.user = user

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        logger.debug(f"Cache miss! Fetching blueprint '{type}'")
        try:
            document: dict = get_document_by_ref(type, self.user)
            return Blueprint(document)
        except Exception as error:
            logger.exception(error)
            raise NotFoundException(message=f"The blueprint '{type}' could not be found")

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_blueprint_provider(user):
    return BlueprintProvider(user)
