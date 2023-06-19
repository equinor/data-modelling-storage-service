from pydantic import conint

from authentication.models import User
from common.reference import Reference
from common.tree_node_serializer import tree_node_to_dict
from domain_classes.tree_node import ListNode, Node
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_document_use_case(
    user: User,
    reference: str,
    depth: conint(gt=-1, lt=1000) = 999,  # type: ignore
    resolve_links: bool = False,
    repository_provider=get_data_source,
):
    """Get document by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    reference_object = Reference.fromabsolute(reference)
    node: Node | ListNode = document_service.get_document(reference_object, depth, resolve_links)
    return tree_node_to_dict(node)
