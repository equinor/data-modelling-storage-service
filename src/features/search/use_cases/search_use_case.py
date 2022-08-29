from copy import deepcopy
from authentication.models import User
from common.exceptions import BadRequestException
from storage.internal.data_source_repository import DataSourceRepository
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from restful.request_types.shared import DataSourceList


class SearchRequest(DataSourceList):
    data: dict
    dotted_attribute_path: str


def get_search_result(output_dict: dict, data_source_id: str, document_service: DocumentService, req: SearchRequest):
    results = document_service.search(
        data_source_id=data_source_id,
        search_data=deepcopy(req.data),
        dotted_attribute_path=req.dotted_attribute_path,
    )
    return output_dict.update(results)


def search_use_case(user: User, request: SearchRequest, repository_provider=get_data_source):
    document_service: DocumentService = DocumentService(repository_provider=repository_provider, user=user)
    all_data_sources = DataSourceRepository(user).list()

    search_results: dict = {}

    if not len(request.data_sources):
        # search all data sources when data_sources list in request is empty.
        for index, data_source in enumerate(all_data_sources):
            data_source_id = data_source["id"]
            get_search_result(search_results, data_source_id, document_service, request)
    else:
        all_data_source_ids: list = [ds["id"] for ds in all_data_sources]
        for data_source in request.data_sources:
            if data_source not in all_data_source_ids:
                raise BadRequestException(f"Data source {data_source} not found")
            get_search_result(search_results, data_source, document_service, request)
    return search_results
