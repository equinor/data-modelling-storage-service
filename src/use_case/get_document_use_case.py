from typing import Optional

from pydantic import conint

from services.document_service import DocumentService
from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class GetDocumentRequest(DataSource):
    document_id: str
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    depth: conint(gt=-1, lt=1000) = 999


class GetDocumentUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider)

    def process_request(self, req: GetDocumentRequest):
        document = self.document_service.get_by_uid(
            data_source_id=req.data_source_id, document_uid=req.document_id, depth=req.depth,
        )

        attribute: str = req.attribute
        if attribute:
            document = document.get_by_path(attribute.split("."))

        return ResponseSuccess({"blueprint": document.blueprint.to_dict_raw(), "document": document.to_dict()})
