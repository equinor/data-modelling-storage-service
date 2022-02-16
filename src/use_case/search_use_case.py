from starlette.responses import JSONResponse

from authentication.models import User
from restful.request_types.shared import DataSource
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


class SearchRequest(DataSource):
    data: dict
    dotted_attribute_path: str


class SearchUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: SearchRequest):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        search_results = document_service.search(
            data_source_id=req.data_source_id, search_data=req.data, dotted_attribute_path=req.dotted_attribute_path
        )
        return JSONResponse(search_results)
