from api.core.storage.internal.data_source_repository import DataSourceRepository


def get_data_source(data_source_id: str):
    return DataSourceRepository().get(data_source_id)
