from authentication.models import User
from common.address import Address
from common.entity.validators import validate_entity_against_self
from common.exceptions import NotFoundException, ValidationException
from services.document_service.document_service import DocumentService


def validate_existing_entity_use_case(address: str, user: User) -> str:
    document_service = DocumentService(user=user)
    try:
        document, _ = document_service.resolve_document(Address.from_absolute(address), depth=500)
    except NotFoundException as ex:
        raise ValidationException(message=ex.message, debug=ex.debug, data=ex.data) from ex
    validate_entity_against_self(document, document_service.get_blueprint)
    return "OK"
