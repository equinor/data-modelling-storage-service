from uuid import uuid4

from authentication.models import User
from enums import SIMOS
from services.document_service.document_service import DocumentService
from storage.internal.get_data_source_cached import get_data_source_cached


def add_raw_bulk_use_case(user: User, documents: list[dict], data_source_id: str) -> list[str]:
    document_repository = get_data_source_cached(data_source_id, user)
    new_node_ids = []
    contains_blueprint = False
    for document in documents:
        new_node_id = document.get("_id", str(uuid4()))
        document["_id"] = new_node_id
        new_node_ids.append(new_node_id)
        contains_blueprint = contains_blueprint or document.get("type") == SIMOS.BLUEPRINT.value
    document_repository.update_many(documents)
    if contains_blueprint:
        DocumentService(user=user).invalidate_cache()
    return new_node_ids
