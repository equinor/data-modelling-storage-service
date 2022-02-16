from typing import List, Optional, Union

from fastapi import File, UploadFile
from starlette.responses import JSONResponse

from authentication.models import User
from restful.request_types.shared import DataSource

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
        if req.attribute and "." in req.document_id:
            raise ValueError(
                "Attribute may only be specified in ether dotted path on "
                + "documentId or the 'attribute' query parameter"
            )
        attribute = req.attribute if req.attribute else ""
        dotted_id = req.document_id + attribute
        document = document_service.update_document(
            data_source_id=req.data_source_id,
            dotted_id=dotted_id,
            data=req.data,
            files={f.filename: f.file for f in req.files} if req.files else None,
            update_uncontained=req.update_uncontained,
        )
        document_service.invalidate_cache()
        return JSONResponse(document)
