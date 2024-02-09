from collections.abc import Callable
from functools import lru_cache, partial

from authentication.models import User
from common.address import Address
from common.exceptions import NotFoundException
from common.providers.address_resolver.address_resolver import (
    ResolvedAddress,
)
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def cached_get_blueprint_with_extended_attributes(
    type: str, get_data_source: Callable, resolve_address: Callable, user: User
) -> Blueprint:
    blueprint: Blueprint = cached_get_blueprint(type, get_data_source, resolve_address, user)

    partial_get_blueprint = partial(
        cached_get_blueprint, get_data_source=get_data_source, resolve_address=resolve_address, user=user
    )
    blueprint.realize_extends(partial_get_blueprint)
    logger.debug(f"Standalone get_extended_blueprint - Cache miss! Fetching extended blueprint '{type}''")
    logger.debug(cached_get_blueprint_with_extended_attributes.cache_info())
    return blueprint


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def cached_get_blueprint(type: str, get_data_source: Callable, resolve_address: Callable, user: User) -> Blueprint:
    logger.debug(f"Standalone get_blueprint - Cache miss! Fetching blueprint '{type}'")
    try:
        resolved_address: ResolvedAddress = resolve_address(
            Address.from_absolute(type),
            lambda data_source_name: get_data_source(data_source_name, user),
        )
    except NotFoundException as ex:
        raise NotFoundException(
            f"Blueprint referenced with '{type}' could not be found. Make sure the reference is correct.",
            data=ex.dict(),
        ) from ex
    resolved_address = resolve_address(
        Address.from_relative(
            resolved_address.entity["address"],
            resolved_address.document_id,
            resolved_address.data_source_id,
        ),
        lambda data_source_name: get_data_source(data_source_name, user),
    )
    return Blueprint(resolved_address.entity, type)
