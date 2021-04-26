from uuid import uuid4

from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from enums import DMT
from services.document_service import DocumentService
from restful import response_object as res
from restful.request_types.shared import DataSource, EntityName
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source
from utils.exceptions import DuplicateFileNameException, FileNotFoundException
from utils.logging import logger
from controllers.package_controller import find_by_name


class AddRootPackageRequest(DataSource, EntityName):
    pass


class AddRootPackageUseCase(UseCase):
    def process_request(self, req: AddRootPackageRequest):
        try:
            find_by_name(req.data_source_id, req.name)
        except FileNotFoundException:
            data = {"name": req.name, "type": DMT.PACKAGE.value, "isRoot": True, "content": []}
            new_node_id = str(uuid4())
            document_service = DocumentService(repository_provider=get_data_source)
            new_node = Node.from_dict(entity=data, uid=new_node_id, blueprint_provider=document_service.get_blueprint)
            document_service.save(node=new_node, data_source_id=req.data_source_id)

            logger.info(f"Added root package '{new_node_id}'")

            return res.ResponseSuccess(DTO(new_node.to_dict()).to_dict())
        else:
            raise DuplicateFileNameException(req.data_source_id, req.name)
