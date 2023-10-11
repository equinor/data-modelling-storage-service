from typing import Callable

from common.providers.address_resolver.address_resolver import ResolvedAddress
from common.providers.reference_resolver import resolve_references_in_entity
from storage.data_source_class import DataSource


def deep_address_resolver(resolved_address: ResolvedAddress, get_data_source: Callable, depth):
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
    return resolved_document
