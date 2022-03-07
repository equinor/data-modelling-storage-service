from starlette.responses import JSONResponse
from copy import deepcopy
from authentication.models import User
import json
from utils.exceptions import BadRequestException
from storage.internal.data_source_repository import DataSourceRepository
from restful.use_case import UseCase
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from pydantic import constr, BaseModel
from restful.request_types.shared import name_regex
from multiprocessing import Manager, Pool
import os


class SearchRequest(BaseModel):
    data: dict
    dotted_attribute_path: str
    data_sources: list[constr(min_length=3, max_length=128, regex=name_regex, strip_whitespace=True)]


def get_search_result(output_dict: dict, data_source_id: str, document_service: DocumentService, req: SearchRequest):
    results = document_service.search(
        data_source_id=data_source_id,
        search_data=deepcopy(req.data),
        dotted_attribute_path=req.dotted_attribute_path,
    )
    return output_dict.update(results)


class SearchUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: SearchRequest):
        document_service: DocumentService = DocumentService(
            repository_provider=self.repository_provider, user=self.user
        )
        all_data_sources = DataSourceRepository(self.user).list()
        all_data_source_names: list = [ds["id"] for ds in all_data_sources]
        manager = Manager()
        search_results: dict = manager.dict()

        pool = Pool(processes=os.cpu_count())

        if not len(req.data_sources):
            # search all data sources when data_sources list in request is empty.
            for i in range(len(all_data_sources)):
                data_source_id = all_data_sources[i]["id"]
                pool.apply_async(get_search_result, [search_results, data_source_id, document_service, req])
        else:
            for i in range(len(req.data_sources)):
                if req.data_sources[i] not in all_data_source_names:
                    raise BadRequestException(f"Data source {req.data_sources[i]} not found")
                pool.apply_async(get_search_result, [search_results, req.data_sources[i], document_service, req])
        pool.close()
        pool.join()
        return JSONResponse(json.loads(json.dumps(search_results.copy())))
