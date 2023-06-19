from authentication.models import User
from common.reference import Reference
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_attribute_use_case(
    reference: str,
    user: User,
    repository_provider=get_data_source,
):
    """Get attribute by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    node: Node = document_service.get_document(Reference.fromabsolute(reference))
    return node.attribute.to_dict()
