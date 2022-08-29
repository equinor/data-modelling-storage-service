from storage.internal.data_source_repository import DataSourceRepository


def get_data_sources_use_case(data_source_repository: DataSourceRepository):
    return data_source_repository.list()
