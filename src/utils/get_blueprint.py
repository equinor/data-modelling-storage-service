from functools import lru_cache

from authentication.models import User
from config import config
from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from utils.exceptions import EntityNotFoundException
from utils.get_document_by_path import get_document_by_ref
from utils.logging import logger


class BlueprintProvider:
    def __init__(self, user: User):
        self.user = user

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        try:
            document: DTO = get_document_by_ref(type, self.user)
            return Blueprint(document)
        except Exception as error:
            logger.exception(error)
            raise EntityNotFoundException(uid=type, message=f"The blueprint '{type}' could not be found")

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.get_blueprint.cache_clear()
        except Exception as error:
            logger.warning("function is not instance of lru cache.", error)
