from functools import lru_cache

from config import config
from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from utils.exceptions import EntityNotFoundException
from utils.find_document_by_path import get_document_by_ref
from utils.logging import logger


class BlueprintProvider:
    @staticmethod
    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(type: str) -> Blueprint:
        try:
            document: DTO = get_document_by_ref(type)
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
