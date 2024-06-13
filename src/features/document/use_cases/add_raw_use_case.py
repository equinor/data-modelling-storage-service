from uuid import uuid4

from authentication.models import User
from domain_classes.storage_recipe import StorageAttribute
from enums import SIMOS, StorageDataTypes
from services.document_service.document_service import DocumentService
from storage.internal.get_data_source_cached import get_data_source_cached


def add_raw_use_case(user: User, document: dict, data_source_id: str):
    new_node_id = document.get("_id", str(uuid4()))
    document["_id"] = new_node_id
    document_repository = get_data_source_cached(data_source_id, user)
    # TODO: This is a problem. Application specific storage recipes are not being used.
    storage_attribute = None
    # Trying to add secrets with 'add_raw' will always use the default strict secret storage recipe
    if document["type"] == SIMOS.SECRET_CONTENT.value:
        storage_attribute = StorageAttribute(
            name="content", contained=False, storage_affinity=StorageDataTypes.SECRET, strict=True
        )
    document_repository.update(document, storage_attribute=storage_attribute)
    if document["type"] == SIMOS.BLUEPRINT.value:
        DocumentService(user=user).invalidate_cache()
    return new_node_id
