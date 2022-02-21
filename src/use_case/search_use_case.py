from starlette.responses import JSONResponse
from copy import deepcopy
from authentication.models import User
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import DataSourceRepository
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from pydantic import constr, BaseModel
from restful.request_types.shared import name_regex


class SearchRequest(BaseModel):
    data: dict
    dotted_attribute_path: str
    data_sources: list[constr(min_length=3, max_length=128, regex=name_regex, strip_whitespace=True)]


class SearchUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: SearchRequest):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        search_results: dict = {}

        if not len(req.data_sources):
            # search all data sources
            all_data_sources = DataSourceRepository(self.user).list()
            for i in range(len(all_data_sources)):
                data_source_id = all_data_sources[i]["id"]
                results = document_service.search(
                    data_source_id=data_source_id,
                    search_data=deepcopy(req.data),
                    dotted_attribute_path=req.dotted_attribute_path,
                )
                search_results.update(results)

        for i in range(len(req.data_sources)):
            # todo check if req.data_sources[i] exists
            # todo if one loop iteration fails due to f ex data source does not exist, a result should still be returned.
            results = document_service.search(
                data_source_id=req.data_sources[i],
                search_data=deepcopy(req.data),
                dotted_attribute_path=req.dotted_attribute_path,
            )
            search_results.update(results)
        return JSONResponse(search_results)
