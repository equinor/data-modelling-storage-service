from typing import Optional

from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.request_types.shared import NamedEntity


class AddToParentRequest(NamedEntity):
    parentId: str
    attribute: str
    description: Optional[str] = ""
    data: Optional[dict] = None
    data_source_id: Optional[str] = None


class AddFileUseCase(uc.UseCase):
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
