from typing import Optional

from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.request_types.shared import DataSource


class UpdateDocumentRequest(DataSource):
    document_id: str
    data: dict
    attribute: Optional[str] = None


class UpdateDocumentUseCase(uc.UseCase):
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
        return res.ResponseSuccess(document)
