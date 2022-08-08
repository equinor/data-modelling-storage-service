from typing import Optional

from authentication.models import User
from restful.use_case import UseCase
from restful.request_types.shared import DataSource
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from common.utils.get_document_by_path import get_document_by_ref


class GetDocumentByPathRequest(DataSource):
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    path: Optional[str] = None


class GetDocumentByPathUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider, user=user)

    def process_request(self, req: GetDocumentByPathRequest):
        data_source_id: str = req.data_source_id
        root_doc = get_document_by_ref(f"{data_source_id}/{req.path}", self.user)
        document = self.document_service.get_node_by_uid(
            data_source_id=req.data_source_id, document_uid=root_doc["_id"]
        )

        if req.attribute:
            document = document.get_by_path(req.attribute.split("."))

        return document.to_dict()
