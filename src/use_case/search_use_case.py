from typing import Optional

from pydantic import BaseModel, Extra

from services.document_service import DocumentService
from restful import response_object as res
from restful.request_types.shared import EntityType
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class SearchDataRequest(EntityType, extra=Extra.allow):
    pass


class SearchRequest(BaseModel):
    data_source_id: Optional[str] = None
    data: SearchDataRequest


class SearchUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: SearchRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        search_results = document_service.search(data_source_id=req.data_source_id, search_data=req.data.dict())
        return res.ResponseSuccess(search_results)
