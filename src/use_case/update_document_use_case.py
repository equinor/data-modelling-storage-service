from typing import List, Optional, Union

from fastapi import File, UploadFile

from domain_classes.user import User
from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class UpdateDocumentRequest(DataSource):
    document_id: str
    data: Union[dict, list]
    attribute: Optional[str] = None
    files: Optional[List[UploadFile]] = File(None)
    update_uncontained: Optional[bool] = True


class UpdateDocumentUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: UpdateDocumentRequest):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        document = document_service.update_document(
            data_source_id=req.data_source_id,
            document_id=req.document_id,
            data=req.data,
            attribute_path=req.attribute,
            files={f.filename: f.file for f in req.files} if req.files else None,
            update_uncontained=req.update_uncontained,
        )
        document_service.invalidate_cache()
        return ResponseSuccess(document)
