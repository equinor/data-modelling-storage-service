from typing import Optional

from domain_classes.user import User
from restful import response_object as res
from restful import use_case as uc
from restful.request_types.shared import DataSource
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from utils.get_document_by_path import get_document_by_ref


class GetDocumentByPathRequest(DataSource):
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    path: Optional[str] = None


class GetDocumentByPathUseCase(uc.UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider, user=user)

    def process_request(self, req: GetDocumentByPathRequest):
        data_source_id: str = req.data_source_id
        root_doc = get_document_by_ref(f"{data_source_id}/{req.path}", self.user)
        document = self.document_service.get_node_by_uid(data_source_id=req.data_source_id, document_uid=root_doc.uid)

        if req.attribute:
            document = document.get_by_path(req.attribute.split("."))

        return res.ResponseSuccess(document.to_dict())
