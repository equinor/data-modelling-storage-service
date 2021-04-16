from typing import Optional

from restful.response_object import ResponseSuccess
from services.document_service import DocumentService
from restful.request_types.shared import DataSource
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class UpdateDocumentRequest(DataSource):
    document_id: str
    data: dict
    attribute: Optional[str] = None


class UpdateDocumentUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: UpdateDocumentRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.update_document(
            data_source_id=req.data_source_id,
            document_id=req.document_id,
            data=req.data,
            attribute_path=req.attribute,
        )
        document_service.invalidate_cache()
        return ResponseSuccess(document)
