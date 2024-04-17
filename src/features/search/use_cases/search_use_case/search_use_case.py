from collections.abc import Callable
from copy import deepcopy

from authentication.models import User
from common.exceptions import ApplicationException, BadRequestException
from common.providers.blueprint_provider import default_blueprint_provider
from common.utils.logging import logger
from features.search.use_cases.search_use_case.build_complex_search import (
    build_mongo_query,
)
from features.search.use_cases.search_use_case.sort_dtos_by_attribute import (
    sort_dtos_by_attribute,
)
from restful.request_types.shared import DataSourceList
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import DataSourceRepository
from storage.internal.get_data_source_cached import get_data_source_cached
from storage.repositories.mongo import MongoDBClient


def _search(
    data_source_id,
    search_data,
    dotted_attribute_path,
    user: User,
    get_data_source: Callable,
):
    repository: DataSource = get_data_source(data_source_id, user)

    if not isinstance(repository.get_default_repository().client, MongoDBClient):
        raise ApplicationException(
            f"Search is not supported on this repository type; {type(repository.repository).__name__}"
        )

    try:
        process_search_data = build_mongo_query(
            default_blueprint_provider.get_blueprint_with_extended_attributes, search_data
        )
    except ValueError as ex:
        logger.warning(f"Failed to build mongo query; {ex}")
        raise BadRequestException("Failed to build mongo query") from ex
    result: list[dict] = repository.find(process_search_data)
    result_sorted: list[dict] = sort_dtos_by_attribute(result, dotted_attribute_path)
    result_list = {}
    for document in result_sorted:
        result_list[f"{data_source_id}/{document['_id']}"] = document

    return result_list


class SearchRequest(DataSourceList):
    data: dict
    dotted_attribute_path: str


def search_use_case(user: User, request: SearchRequest) -> dict:
    all_data_source_ids = [ds["id"] for ds in DataSourceRepository(user).list()]
    search_data_sources = all_data_source_ids

    if request.data_sources:
        # If user has specified any data sources, check that they exist, then select only through them for search.
        if invalid_search_data_sources := set(request.data_sources) - set(all_data_source_ids):
            formatted_ids = "\n\t" + "\n\t".join(invalid_search_data_sources)
            raise BadRequestException(f"Data sources not found:{formatted_ids}")
        search_data_sources = request.data_sources

    search_results: dict = {}
    for data_source_id in search_data_sources:
        results = _search(
            data_source_id=data_source_id,
            search_data=deepcopy(request.data),
            dotted_attribute_path=request.dotted_attribute_path,
            user=user,
            get_data_source=get_data_source_cached,
        )
        search_results.update(results)
    return search_results
