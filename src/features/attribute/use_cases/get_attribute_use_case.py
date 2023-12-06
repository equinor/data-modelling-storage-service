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
        # type: ignore
        reference_node: Node = document_service.get_document(
            Address.from_relative(direct_address, None, Address.from_absolute(address).data_source), 2
        )
        return {"attribute": reference_node.attribute.to_dict(), "address": direct_address}
    return {"attribute": node.attribute.to_dict(), "address": direct_address}
