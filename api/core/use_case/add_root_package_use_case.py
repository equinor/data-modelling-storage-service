from uuid import uuid4

from api.classes.dto import DTO
from api.classes.tree_node import Node
from api.core.enums import DMT
from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.core.storage.repository_exceptions import DuplicateFileNameException, FileNotFoundException
from api.core.utility import BlueprintProvider
from api.request_types.shared import DataSource, EntityName
from api.utils.logging import logger
from controllers.package_controller import find_by_name


class AddRootPackageRequest(DataSource, EntityName):
    pass


class AddRootPackageUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, req: AddRootPackageRequest):
        try:
            find_by_name(req.data_source_id, req.name)
        except FileNotFoundException:
            data = {"name": req.name, "type": DMT.PACKAGE.value, "isRoot": True, "content": []}
            new_node_id = str(uuid4())
            new_node = Node.from_dict(entity=data, uid=new_node_id, blueprint_provider=self.blueprint_provider)
            document_service = DocumentService(repository_provider=get_data_source)
            document_service.save(node=new_node, data_source_id=req.data_source_id)

            logger.info(f"Added root package '{new_node_id}'")

            return res.ResponseSuccess(DTO(new_node.to_dict()).to_dict())
        else:
            raise DuplicateFileNameException(req.data_source_id, req.name)
