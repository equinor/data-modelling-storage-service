from typing import Optional

from services.document_service import DocumentService
from restful import response_object as res
from restful.request_types.shared import NamedEntity
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class AddToParentRequest(NamedEntity):
    parentId: str
    attribute: str
    type: str
    description: Optional[str] = ""
    data: Optional[dict] = None
    data_source_id: Optional[str] = None


class AddFileUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: AddToParentRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.add_document(
            data_source_id=req.data_source_id,
            parent_id=req.parentId,
            type=req.type,
            name=req.name,
            description=req.description,
            attribute_path=req.attribute,
        )
        document_service.invalidate_cache()
        return res.ResponseSuccess(document)
