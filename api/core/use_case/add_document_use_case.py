from uuid import uuid4

from api.classes.tree_node import Node
from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.core.utility import BlueprintProvider
from api.request_types.shared import DataSource, NamedEntity


class AddDocumentRequest(DataSource):
    data: NamedEntity


class AddDocumentUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, req: AddDocumentRequest):
        data = req.data.dict()
        new_node_id = str(uuid4()) if "_id" not in data else data["_id"]
        new_node = Node.from_dict(data, new_node_id, self.blueprint_provider)
        document_service = DocumentService(repository_provider=get_data_source)
        document_service.save(node=new_node, data_source_id=req.data_source_id)

        return res.ResponseSuccess(new_node_id)
