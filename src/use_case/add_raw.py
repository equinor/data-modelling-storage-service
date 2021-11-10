from uuid import uuid4
from domain_classes.user import User
from domain_classes.dto import DTO
from enums import SIMOS
from restful import response_object as res
from restful.request_types.shared import DataSource, UncontainedEntity
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from utils.validators import entity_has_all_required_attributes


class AddRawRequest(DataSource):
    document: UncontainedEntity


class AddRawUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: AddRawRequest):
        new_node_id = req.document.dict(by_alias=True).get("_id", str(uuid4()))
        dict = req.document.to_dict()
        document: DTO = DTO(uid=new_node_id, data=dict)
        document_repository = get_data_source(req.data_source_id, self.user)
        document_service = DocumentService(user=self.user)
        blueprint = document_service.get_blueprint(dict["type"])
        required_attributes = blueprint.get_required_attributes()
        entity_has_all_required_attributes(entity=dict, required_attributes=required_attributes)

        document_repository.update(document)
        if document.type == SIMOS.BLUEPRINT.value:
            DocumentService(user=self.user).invalidate_cache()
        return res.ResponseSuccess(new_node_id)
