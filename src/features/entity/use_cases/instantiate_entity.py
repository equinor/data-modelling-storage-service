from authentication.models import User
from common.utils.create_entity import CreateEntity
from services.document_service import DocumentService


def instantiate_entity_use_case(blueprint_type: str, user: User) -> dict:
    document_service = DocumentService(user=user)
    document: dict = CreateEntity(document_service.get_blueprint, blueprint_type).entity
    return document
