from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import DataSourceRepository


def get_data_source_use_case(data_source: DataSource, data_source_repository: DataSourceRepository):
    data_source = data_source_repository.get(data_source.data_source_id)
    return {"name": data_source.name, "id": data_source.name}
