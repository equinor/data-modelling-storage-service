from typing import Callable

from common.address import Address
from common.providers.address_resolver.address_resolver import (
    ResolvedAddress,
    resolve_address,
)
from common.providers.address_resolver.reference_resolver import (
    resolve_references_in_entity,
)
from storage.data_source_class import DataSource


def deep_address_resolver(address: Address, get_data_source: Callable, depth):
    resolved_address: ResolvedAddress = resolve_address(address, get_data_source)

    data_source: DataSource = get_data_source(resolved_address.data_source_id)
    document: dict = data_source.get(resolved_address.document_id)

    resolved_document: dict = resolve_references_in_entity(
        document,
        data_source,
        get_data_source,
        resolved_address.document_id,
        depth=depth + len(list(filter(lambda x: x[0] != "[", resolved_address.attribute_path))),
        depth_count=1,
    )
    return ResolvedAddress(
        entity=resolved_document,
        document_id=resolved_address.document_id,
        attribute_path=resolved_address.attribute_path,
        data_source_id=resolved_address.data_source_id,
    )
