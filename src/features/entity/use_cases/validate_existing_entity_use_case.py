from authentication.models import User
from common.address import Address
from common.entity.validators import validate_entity_against_self
from common.exceptions import NotFoundException, ValidationException
from common.tree.tree_node import Node
from services.document_service.document_service import DocumentService


def validate_existing_entity_use_case(address: str, user: User) -> str:
    document_service = DocumentService(user=user)
    try:
        document_as_node: Node = document_service.get_document(Address.from_absolute(address), depth=500)
    except NotFoundException as ex:
        raise ValidationException(message=ex.message, debug=ex.debug) from ex
    validate_entity_against_self(document_as_node.entity, document_service.get_blueprint)
    return "OK"
