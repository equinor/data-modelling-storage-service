from uuid import uuid4

from domain_classes.tree_node import Node
from services.document_service import DocumentService
from restful import response_object as res
from restful.request_types.shared import DataSource, NamedEntity
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class AddDocumentRequest(DataSource):
    data: NamedEntity


class AddDocumentUseCase(UseCase):
    def process_request(self, req: AddDocumentRequest):
        data = req.data.dict()
        document_service = DocumentService(repository_provider=get_data_source)
        new_node_id = str(uuid4()) if "_id" not in data else data["_id"]
        new_node = Node.from_dict(data, new_node_id, document_service.get_blueprint)
        document_service.save(node=new_node, data_source_id=req.data_source_id)

        return res.ResponseSuccess(new_node_id)
