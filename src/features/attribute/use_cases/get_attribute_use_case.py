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
    if resolve and node.attribute.attribute_type == SIMOS.REFERENCE.value:
        reference_address = Address.from_relative(
            node.entity["address"], node.find_parent().node_id, node.get_data_source()
        )
        # Resolve the reference
        reference_node: Node = document_service.get_document(reference_address, 1)
        return {"attribute": reference_node.attribute.to_dict(), "address": str(reference_address)}
    return {"attribute": node.attribute.to_dict(), "address": address}
