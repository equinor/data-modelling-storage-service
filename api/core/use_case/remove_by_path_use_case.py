from typing import Optional

from pydantic.main import BaseModel

from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source


class RemoveByPathRequest(BaseModel):
    directory: str
    data_source_id: Optional[str] = None


class RemoveByPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: RemoveByPathRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        document_service.remove_by_path(req.data_source_id, req.directory)
        document_service.invalidate_cache()
        return res.ResponseSuccess(True)
