from api.classes.data_source import DataSourceFactory, DataSource
from api.core.repository import Repository


def get_repository(data_source_id: str):
    data_source_factory = DataSourceFactory()
    data_source: DataSource = data_source_factory.get_data_source(data_source_id)
    return Repository(
        name=data_source.name,
        db=data_source.get_client(),
        document_type=data_source.document_type,
    )
