from authentication.models import User
from common.entity.validators import validate_entity, validate_entity_against_self
from restful.request_types.shared import Entity, TypeConstrainedString
from services.document_service.document_service import DocumentService


def validate_entity_use_case(entity: Entity, user: User, as_type: TypeConstrainedString | None) -> str:
    document_service = DocumentService(user=user)
    if as_type:
        validate_entity(
            entity.dict(), document_service.get_blueprint, document_service.get_blueprint(as_type), "minimum"
        )
    validate_entity_against_self(entity.dict(), document_service.get_blueprint)
    return "OK"
