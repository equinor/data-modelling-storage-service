from copy import deepcopy

from authentication.models import User
from common.exceptions import BadRequestException
from restful.request_types.shared import DataSourceList
from services.document_service import DocumentService
from storage.internal.data_source_repository import (
    DataSourceRepository,
    get_data_source,
)


class SearchRequest(DataSourceList):
    data: dict
    dotted_attribute_path: str


def search_use_case(user: User, request: SearchRequest, repository_provider=get_data_source) -> dict:
    document_service: DocumentService = DocumentService(repository_provider=repository_provider, user=user)
    all_data_source_ids = [ds["id"] for ds in DataSourceRepository(user).list()]
    search_data_sources = all_data_source_ids

    if request.data_sources:
        # If user has specified any data sources, check that they exist, then select only through them for search.
        if invalid_search_data_sources := set(request.data_sources) - set(all_data_source_ids):
            raise BadRequestException(f"Data source {invalid_search_data_sources.pop()} not found")
        search_data_sources = request.data_sources

    search_results: dict = {}
    for data_source_id in search_data_sources:
        results = document_service.search(
            data_source_id=data_source_id,
            search_data=deepcopy(request.data),
            dotted_attribute_path=request.dotted_attribute_path,
        )
        search_results.update(results)
    return search_results
