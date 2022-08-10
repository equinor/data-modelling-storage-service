from restful.request_types.create_data_source import DataSourceRequest
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import DataSourceRepository


def create_data_source_use_case(
    data_source_repository: DataSourceRepository, data_source_id: DataSource, new_data_source: DataSourceRequest
):
    response = data_source_repository.create(data_source_id, new_data_source)
    return response
