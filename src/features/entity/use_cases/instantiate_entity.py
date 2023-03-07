from authentication.models import User
from common.utils.create_entity import CreateEntity
from restful.request_types.shared import Entity
from services.document_service import DocumentService


def instantiate_entity_use_case(basic_entity: Entity, user: User) -> dict:
    document_service = DocumentService(user=user)
    document: dict = CreateEntity(document_service.get_blueprint, basic_entity.type).entity
    return document
