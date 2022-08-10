from uuid import uuid4
from authentication.models import User
from enums import SIMOS
from restful.request_types.shared import UncontainedEntity
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


# todo data_source_id as DataSource type?
def add_raw_use_case(user: User, document: UncontainedEntity, data_source_id: str):
    new_node_id = document.dict(by_alias=True).get("_id", str(uuid4()))
    document = document.to_dict()
    document["_id"] = new_node_id
    document_repository = get_data_source(data_source_id, user)
    document_repository.update(document)
    if document["type"] == SIMOS.BLUEPRINT.value:
        DocumentService(user=user).invalidate_cache()
    return new_node_id
