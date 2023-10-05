from authentication.models import User
from common.address import Address
from common.entity.validators import validate_entity_against_self
from common.tree.tree_node import Node
from services.document_service.document_service import DocumentService


def validate_existing_entity_use_case(address: str, user: User) -> str:
    document_service = DocumentService(user=user)
    document_as_node: Node = document_service.get_document(Address.from_absolute(address), depth=999)
    # TODO resolving fails in above line. for some reason the address dmss://DemoDataSource/plugins/DemoDataSource/plugins/grid/blueprints/Dashboard
    validate_entity_against_self(document_as_node.entity, document_service.get_blueprint)
    return "OK"
