from api.core.enums import PRIMITIVES
from api.core.repository.repository_factory import get_repository
from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.utility import get_document_by_ref

from api.classes.blueprint_attribute import BlueprintAttribute
from api.classes.dto import DTO
from api.utils.logging import logger


class GetDocumentRequestObject(req.ValidRequestObject):
    def __init__(self, data_source_id, document_id, ui_recipe, attribute):
        self.data_source_id = data_source_id
        self.document_id = document_id
        self.ui_recipe = ui_recipe
        self.attribute = attribute

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if "document_id" not in adict:
            invalid_req.add_error("document_id", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            data_source_id=adict.get("data_source_id"),
            document_id=adict.get("document_id"),
            ui_recipe=adict.get("ui_recipe"),
            attribute=adict.get("attribute"),
        )


class GetDocumentUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_repository):
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider)

    def process_request(self, request_object: GetDocumentRequestObject):
        data_source_id: str = request_object.data_source_id
        document_id: str = request_object.document_id
        attribute: str = request_object.attribute

        document = self.document_service.get_by_uid(data_source_id=data_source_id, document_uid=document_id)

        if attribute:
            document = document.get_by_path(attribute.split("."))

        return res.ResponseSuccess({"blueprint": document.blueprint.to_dict_raw(), "document": document.to_dict()})
