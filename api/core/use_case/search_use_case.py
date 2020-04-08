from api.core.repository.repository_factory import get_repository
from api.core.service.document_service import DocumentService
from api.core.shared import response_object as res
from api.core.shared import use_case as uc


class SearchUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_repository):
        self.repository_provider = repository_provider

    def process_request(self, request_object):
        data_source_id = request_object["data_source_id"]
        search_data = request_object["data"]

        document_service = DocumentService(repository_provider=self.repository_provider)
        search_results = document_service.search(data_source_id=data_source_id, search_data=search_data)
        return res.ResponseSuccess(search_results)
