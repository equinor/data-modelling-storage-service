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
from utils.exceptions import DuplicateFileNameException
from utils.logging import logger


class AddRootPackageRequest(EntityName, extra=Extra.allow):
    pass


class AddRootPackageUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: dict):
        exisiting_root_package = get_data_source(req["data_source_id"], self.user).find(
            {"type": "system/SIMOS/Package", "isRoot": True, "name": req["name"]}
        )

        if not exisiting_root_package:
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
