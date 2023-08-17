from authentication.models import User
from common.utils.validators import validate_entity, validate_entity_against_self
from restful.request_types.shared import Entity, common_type_constrained_string
from services.document_service import DocumentService


def validate_entity_use_case(entity: Entity, user: User, as_type: common_type_constrained_string | None) -> str:
    document_service = DocumentService(user=user)
    if as_type:
        validate_entity(
            entity.dict(), document_service.get_blueprint, document_service.get_blueprint(as_type), "minimum"
        )
    validate_entity_against_self(entity.dict(), document_service.get_blueprint)
    return "OK"
