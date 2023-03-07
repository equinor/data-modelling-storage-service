from authentication.models import User
from common.utils.validators import validate_entity
from restful.request_types.shared import Entity, common_type_constrained_string
from services.document_service import DocumentService


def validate_entity_use_case(entity: Entity, user: User, as_type: common_type_constrained_string | None) -> str:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(as_type if as_type else entity.type)
    validate_entity(entity.dict(), blueprint, document_service.get_blueprint, allow_extra=bool(as_type))
    return "OK"
