from authentication.models import User
from common.utils.validators import validate_entity
from restful.request_types.shared import Entity
from services.document_service import DocumentService


def validate_entity_use_case(entity: Entity, user: User) -> str:
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(entity.type)
    validate_entity(entity.dict(), blueprint, document_service.get_blueprint)
    return "OK"
