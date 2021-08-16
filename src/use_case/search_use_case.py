from restful import response_object as res
from restful.request_types.shared import DataSource
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class SearchRequest(DataSource):
    data: dict
    sort_by_attribute: str


class SearchUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: SearchRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        search_results = document_service.search(
            data_source_id=req.data_source_id, search_data=req.data, sort_by_attribute=req.sort_by_attribute
        )
        return res.ResponseSuccess(search_results)
