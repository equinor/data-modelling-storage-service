from uuid import uuid4

from api.core.service.document_service import DocumentService

from api.classes.dto import DTO
from api.core.enums import DMT
from api.core.storage.data_source import DataSource
from api.core.storage.repository_exceptions import DuplicateFileNameException, FileNotFoundException
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.utils.logging import logger
from controllers.package_controller import find_by_name
from api.core.storage.internal.data_source_repository import get_data_source
from api.classes.tree_node import Node
from api.core.utility import BlueprintProvider


class AddRootPackageRequestObject(req.ValidRequestObject):
    def __init__(self, name=None, data_source_id=None):
        self.name = name
        self.data_source_id = data_source_id

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "name" not in adict or len(adict["name"]) == 0:
            invalid_req.add_error("name", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(name=adict.get("name"), data_source_id=adict.get("data_source_id"))


class AddRootPackageUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, request_object):
        name: str = request_object.name
        data_source_id: str = request_object.data_source_id

        try:
            find_by_name(data_source_id, name)
        except FileNotFoundException:
            data = {"name": name, "type": DMT.PACKAGE.value, "isRoot": True, "content": []}
            new_node_id = str(uuid4()) if "_id" not in data else data["_id"]
            new_node = Node.from_dict(entity=data, uid=new_node_id, blueprint_provider=self.blueprint_provider)
            document_service = DocumentService(repository_provider=get_data_source)
            document_service.save(node=new_node, data_source_id=data_source_id)

            logger.info(f"Added root package '{new_node_id}'")

            return res.ResponseSuccess(DTO(new_node.to_dict()).to_dict())
        else:
            raise DuplicateFileNameException(self.data_source_id, name)
