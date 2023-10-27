from authentication.models import User
from common.address import Address
from common.tree.tree_node import Node
from enums import SIMOS
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_attribute_use_case(
    address: str,
    resolve: bool,
    user: User,
    repository_provider=get_data_source,
):
    """Get attribute by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    node: Node = document_service.get_document(Address.from_absolute(address))
    direct_address = address
    if resolve and node.attribute.attribute_type == SIMOS.REFERENCE.value:
        direct_address = node.entity["address"]
        node: Node = document_service.get_document(Address.from_absolute(direct_address), 2)  # type: ignore
    return {"attribute": node.attribute.to_dict(), "address": direct_address}
