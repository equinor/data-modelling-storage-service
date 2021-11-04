from pydantic.main import BaseModel

from domain_classes.user import User
from services.document_service import DocumentService
from restful import response_object as res
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class RemoveRequest(BaseModel):
    documentId: str
    data_source_id: str


class RemoveUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: RemoveRequest):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        document_service.remove_document(req.data_source_id, req.documentId)
        document_service.invalidate_cache()
        return res.ResponseSuccess(True)
