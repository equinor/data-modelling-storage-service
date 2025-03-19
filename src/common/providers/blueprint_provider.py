import uuid
from collections.abc import Callable
from functools import lru_cache

from authentication.models import User
from common.address import Address
from common.exceptions import ApplicationException, NotFoundException
from common.providers.address_resolver.address_resolver import (
    resolve_address,
)
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from enums import SIMOS
from storage.data_source_interface import DataSource
from storage.internal.data_source_repository import get_data_source


def substitute_get_blueprint(*args, **kwargs):
    raise ValueError("'get_blueprint' should not be called when fetching blueprints")


def find_entity_by_name_in_package(
    package: dict,
    path_elements: list[str],
    data_source: str,
    get_data_source: Callable,
    cache: dict,
    concated_path: str,
) -> dict:
    for reference in package.get("content", []):
        resolved_reference = resolve_address(Address(reference["address"], data_source), get_data_source).entity

        # Add resolved reference to cache if they are blueprints
        if resolved_reference["type"] in (SIMOS.BLUEPRINT.value, SIMOS.ENUM.value):
            cache[f"{concated_path}/{resolved_reference['name']}"] = resolved_reference
            if len(path_elements) == 1 and resolved_reference.get("name") == path_elements[0]:
                return resolved_reference

        if resolved_reference.get("name") == path_elements[0] and len(path_elements) > 1:
            return find_entity_by_name_in_package(
                resolved_reference,
                path_elements[1:],
                data_source,
                get_data_source,
                cache,
                f"{concated_path}/{resolved_reference['name']}",
            )

    raise NotFoundException(f"Could not find entity with name '{path_elements[0]}' in package '{package['name']}'")


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
        # Fetched blueprint documents are cached in this object, even before they are requested
        self.prefetched_blueprints: dict[str, dict] = {}

    @lru_cache(maxsize=128)  # noqa B019
    def get_data_source_cached(self, data_source_id: str) -> DataSource:
        # BlueprintProvider needs its own  'get_data_source' function to avoid circular imports
        return self.get_data_source(data_source_id, self.user, substitute_get_blueprint)

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)  # noqa: B019
    def get_blueprint_with_extended_attributes(self, type: str) -> Blueprint:
        blueprint: Blueprint = self.get_blueprint(type)
        blueprint.realize_extends(self.get_blueprint)
        return blueprint

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)  # noqa: B019
    def get_blueprint(self, type: str) -> Blueprint:
        """Custom 'get_document' function that caches the fetched blueprints,
        even if they were not the requested blueprint.
        This is done for performance optimization, as often, all blueprints are requested at one point.
        Only supports references on the "path" format.
        """
        if type in self.prefetched_blueprints:
            logger.debug(f"Cache hit! Returning pre-fetched blueprint '{type}'")
            return Blueprint(self.prefetched_blueprints[type], type)
        try:
            logger.debug(f"Cache miss! Fetching blueprint '{type}' '{hash(self)}'")
            address = Address.from_absolute(type)
            data_source = self.get_data_source_cached(address.data_source)
            path_elements = address.path.split("/")
            query = {"name": path_elements[0], "type": SIMOS.PACKAGE.value, "isRoot": True}
            root_package = data_source.find(query)
            if not root_package:
                # Sometimes the find query returns an empty list,
                # even if the package exists, so need to call find query twice.
                root_package = data_source.find(query)
            if not root_package:
                raise NotFoundException(f"Could not find root package '{path_elements[0]}'")
            if len(root_package) > 1:
                raise ApplicationException(f"Multiple root packages found with name '{path_elements[0]}'")
            return Blueprint(
                find_entity_by_name_in_package(
                    root_package[0],
                    path_elements[1:],
                    address.data_source,
                    get_data_source=lambda data_source_name: self.get_data_source_cached(data_source_name),
                    cache=self.prefetched_blueprints,
                    concated_path=f"dmss://{address.data_source}/{path_elements[0]}",
                ),
                type,
            )

        except NotFoundException as ex:
            raise NotFoundException(
                f"Blueprint referenced with '{type}' could not be found. Make sure the reference is correct.",
                data=ex.dict(),
            ) from ex

    def invalidate_cache(self):
        try:
            logger.debug("invalidate cache")
            self.prefetched_blueprints = {}
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
