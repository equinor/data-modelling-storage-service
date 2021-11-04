from uuid import uuid4

from pydantic import Extra

from domain_classes.user import User
from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from enums import DMT
from services.document_service import DocumentService
from restful import response_object as res
from restful.request_types.shared import EntityName
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source
from utils.exceptions import DuplicateFileNameException, FileNotFoundException
from utils.logging import logger
from controllers.package_controller import find_by_name


class AddRootPackageRequest(EntityName, extra=Extra.allow):
    pass


class AddRootPackageUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: dict):
        try:
            find_by_name(req["data_source_id"], req["name"], self.user)
        except FileNotFoundException:
            data = {
                "_id": req.get("_id", str(uuid4())),
                "name": req["name"],
                "type": DMT.PACKAGE.value,
                "isRoot": True,
                "content": [],
            }
            document_service = DocumentService(repository_provider=get_data_source, user=self.user)
            new_node = Node.from_dict(entity=data, uid=data["_id"], blueprint_provider=document_service.get_blueprint)
            document_service.save(node=new_node, data_source_id=req["data_source_id"])

            logger.info(f"Added root package '{new_node.name} - {new_node.uid}'")

            return res.ResponseSuccess(DTO(new_node.to_dict()).to_dict())
        else:
            raise DuplicateFileNameException(req["data_source_id"], req["name"])
