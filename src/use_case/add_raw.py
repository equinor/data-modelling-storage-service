from uuid import uuid4

from domain_classes.dto import DTO
from enums import SIMOS
from restful import response_object as res
from restful.request_types.shared import DataSource, UncontainedEntity
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class AddRawRequest(DataSource):
    document: UncontainedEntity


class AddRawUseCase(UseCase):
    def process_request(self, req: AddRawRequest):
        new_node_id = req.document.dict(by_alias=True).get("_id", str(uuid4()))
        document: DTO = DTO(uid=new_node_id, data=req.document.dict())
        document_repository = get_data_source(req.data_source_id)
        document_repository.add(document)
        if document.type == SIMOS.BLUEPRINT.value:
            DocumentService().invalidate_cache()
        return res.ResponseSuccess(new_node_id)
