from typing import Optional

from pydantic.main import BaseModel
from starlette.responses import PlainTextResponse

from authentication.models import User
from services.document_service import DocumentService
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class RemoveByPathRequest(BaseModel):
    directory: str
    data_source_id: Optional[str] = None


class RemoveByPathUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: RemoveByPathRequest):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        document_service.remove_by_path(req.data_source_id, req.directory)
        document_service.invalidate_cache()
        return PlainTextResponse("OK")
