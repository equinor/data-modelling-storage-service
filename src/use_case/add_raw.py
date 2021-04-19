from uuid import uuid4

from domain_classes.dto import DTO
from restful import response_object as res
from restful.request_types.shared import DataSource, NamedEntity
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class AddRawRequest(DataSource):
    document: NamedEntity


class AddRawUseCase(UseCase):
    def process_request(self, req: AddRawRequest):
        uid: str = req.document.uid
        new_node_id = str(uuid4()) if not uid else uid
        document: DTO = DTO(uid=new_node_id, data=req.document.dict())
        document_repository = get_data_source(req.data_source_id)
        document_repository.add(document)
        return res.ResponseSuccess(new_node_id)
