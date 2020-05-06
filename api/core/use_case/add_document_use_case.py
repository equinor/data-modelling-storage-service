from typing import Dict
from uuid import uuid4

from api.core.utility import BlueprintProvider

from api.classes.tree_node import Node
from api.core.repository.repository_factory import get_repository
from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc


class AddDocumentRequestObject(req.ValidRequestObject):
    def __init__(self, uid=None, data=None, data_source_id=None):
        self.uid = uid
        self.data = data
        self.data_source_id = data_source_id

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "data" not in adict:
            invalid_req.add_error("data", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(uid=adict.get("uid", None), data=adict.get("data"), data_source_id=adict.get("data_source_id"))


class AddDocumentUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, request_object):
        data: Dict = request_object.data
        data_source_id: str = request_object.data_source_id

        new_node_id = str(uuid4()) if "_id" not in data else data["_id"]
        new_node = Node.from_dict(data, new_node_id, self.blueprint_provider)
        document_service = DocumentService(repository_provider=get_repository)
        document_service.save(node=new_node, data_source_id=data_source_id)

        return res.ResponseSuccess(new_node_id)
