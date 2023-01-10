from typing import Optional

from pydantic import BaseModel
from pydantic.config import Extra

from authentication.models import User
from common.utils.create_entity import CreateEntity
from services.document_service import DocumentService


class BasicEntity(BaseModel, extra=Extra.allow):  # type: ignore
    name: Optional[str] = None
    type: str


def instantiate_entity_use_case(basic_entity: BasicEntity, user: User) -> dict:
    document_service = DocumentService(user=user)
    document: dict = CreateEntity(document_service.get_blueprint, basic_entity.type, name=basic_entity.name).entity
    return document
