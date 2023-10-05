from uuid import uuid4

from authentication.models import User
from enums import SIMOS
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def add_raw_use_case(user: User, document: dict, data_source_id: str):
    new_node_id = document.get("_id", str(uuid4()))
    document["_id"] = new_node_id
    document_repository = get_data_source(data_source_id, user)
    document_repository.update(document)
    if document["type"] == SIMOS.BLUEPRINT.value:
        DocumentService(user=user).invalidate_cache()
    return new_node_id
