from authentication.models import User

from restful.request_types.shared import EntityType
from services.document_service import DocumentService


def get_blueprint_use_case(user: User, entity_type: EntityType):
    document_service = DocumentService(user=user)
    blueprint = document_service.get_blueprint(entity_type)
    return blueprint.to_dict()
