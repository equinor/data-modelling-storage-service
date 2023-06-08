from authentication.models import User
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
    if "://" not in reference:
        reference = f"/{reference}"
    node: Node = document_service.get_document(reference)
    return node.attribute.to_dict()
