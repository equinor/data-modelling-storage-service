from authentication.models import User
from common.tree_node_serializer import tree_node_to_dict
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_document_by_path_use_case(
    user: User,
    absolute_path: str,
    repository_provider=get_data_source,
):
    """Fetch an entity based on 'absolute path'.
    The format would look like; PROTOCOL://ROOT_PACKAGE/ENTITY.Attribute"""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    if "://" not in absolute_path:
        absolute_path = f"/{absolute_path}"
    node: Node = document_service.get_document(absolute_path)
    return tree_node_to_dict(node)
