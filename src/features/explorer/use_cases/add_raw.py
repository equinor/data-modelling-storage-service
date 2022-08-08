from uuid import uuid4

from authentication.models import User

from enums import SIMOS
from restful.request_types.shared import DataSource, UncontainedEntity
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class AddRawRequest(DataSource):
    document: UncontainedEntity


class AddRawUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: AddRawRequest):
        new_node_id = req.document.dict(by_alias=True).get("_id", str(uuid4()))
        document = req.document.to_dict()
        document["_id"] = new_node_id
        document_repository = get_data_source(req.data_source_id, self.user)
        document_repository.update(document)
        if document["type"] == SIMOS.BLUEPRINT.value:
            DocumentService(user=self.user).invalidate_cache()
        return new_node_id
