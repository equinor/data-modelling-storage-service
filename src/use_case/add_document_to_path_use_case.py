from typing import List, Optional

from fastapi import UploadFile
from pydantic import validator

from restful.request_types.shared import DataSource, NamedEntity
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class AddDocumentToPathRequest(DataSource):
    document: NamedEntity
    directory: str
    files: Optional[List[UploadFile]] = None

    @validator("directory", always=True)
    def validate_directory(cls, value):
        return value.removeprefix("/").removesuffix("/")


class AddDocumentToPathUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: AddDocumentToPathRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.add(
            data_source_id=req.data_source_id,
            path=req.directory,
            document=req.document,
            files={f.filename: f.file for f in req.files} if req.files else None,
        )
        return ResponseSuccess(document)
