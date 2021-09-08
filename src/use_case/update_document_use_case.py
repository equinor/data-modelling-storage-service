from typing import List, Optional

from fastapi import File, UploadFile

from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class UpdateDocumentRequest(DataSource):
    document_id: str
    data: dict
    attribute: Optional[str] = None
    files: Optional[List[UploadFile]] = File(None)


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
            files={f.filename: f.file for f in req.files} if req.files else None,
        )
        document_service.invalidate_cache()
        return ResponseSuccess(document)
