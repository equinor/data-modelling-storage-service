from typing import List, Optional

from fastapi import File, UploadFile
from pydantic import validator

from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.request_types.shared import DataSource


class AddDocumentToPathRequest(DataSource):
    document: dict
    directory: str
    files: Optional[List[UploadFile]] = File(None)

    @validator("directory", always=True)
    def validate_directory(cls, value):
        return value.removeprefix("/").removesuffix("/")


class AddDocumentToPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: AddDocumentToPathRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.add(
            data_source_id=req.data_source_id,
            directory=req.directory,
            document=req.document,
            files={f.filename: f.file for f in req.files},
        )
        return res.ResponseSuccess(document)
