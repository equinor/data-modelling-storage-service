from typing import Annotated

from pydantic import Field

from authentication.models import User
from common.address import Address
from common.tree.tree_node import ListNode, Node
from common.tree.tree_node_serializer import tree_node_to_dict
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_document_use_case(
    user: User,
    address: str,
    depth: Annotated[int, Field(gt=-1, lt=1000)],  # type: ignore
    repository_provider=get_data_source,
):
    """Get document by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    address_object = Address.from_absolute(address)
    node: Node | ListNode = document_service.get_document(address_object, depth)
    return tree_node_to_dict(node)
