from typing import Optional

from api.core.storage.internal.data_source_repository import get_data_source
from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.utility import get_document_by_ref
from api.request_types.shared import DataSource


class GetDocumentByPathRequest(DataSource):
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    path: Optional[str] = None


class GetDocumentByPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider)

    def process_request(self, req: GetDocumentByPathRequest):
        data_source_id: str = req.data_source_id
        root_doc = get_document_by_ref(f"{data_source_id}/{req.path}")
        document = self.document_service.get_by_uid(data_source_id=req.data_source_id, document_uid=root_doc.uid)

        if req.attribute:
            document = document.get_by_path(req.attribute.split("."))

        return res.ResponseSuccess({"document": document.to_dict()})
