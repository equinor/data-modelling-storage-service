from typing import Dict
from uuid import uuid4

from api.classes.dto import DTO
from api.core.storage.data_source import DataSource
from api.core.storage.internal.data_source_repository import get_data_source
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.utility import BlueprintProvider


class AddRawRequestObject(req.ValidRequestObject):
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


class AddRawUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, request_object):
        data: Dict = request_object.data
        data_source_id: str = request_object.data_source_id
        uid: str = request_object.uid
        new_node_id = str(uuid4()) if not uid else uid
        document: DTO = DTO(uid=new_node_id, data=data)
        document_repository: DataSource = get_data_source(data_source_id)
        document_repository.add(document)

        return res.ResponseSuccess(new_node_id)
