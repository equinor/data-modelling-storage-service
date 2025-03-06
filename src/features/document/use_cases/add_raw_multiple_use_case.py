from uuid import uuid4

from authentication.models import User
from enums import SIMOS
from services.document_service.document_service import DocumentService
from storage.internal.get_data_source_cached import get_data_source_cached


def add_raw_multiple_use_case(user: User, documents: list[dict], data_source_id: str):
    document_repository = get_data_source_cached(data_source_id, user)
    invalid_cache = False
    for document in documents:
        new_node_id = document.get("_id", str(uuid4()))
        document["_id"] = new_node_id
        document_repository.update(document)
        if document["type"] == SIMOS.BLUEPRINT.value:
            invalid_cache = True
    if invalid_cache:
        DocumentService(user=user).invalidate_cache()
    return [document["_id"] for document in documents]
