from typing import Optional

from pydantic import conint

from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.request_types.shared import DataSource


class GetDocumentRequest(DataSource):
    document_id: str
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    depth: conint(gt=-1, lt=1000) = 999


class GetDocumentUseCase(uc.UseCase):
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

        return res.ResponseSuccess({"blueprint": document.blueprint.to_dict_raw(), "document": document.to_dict()})
