from functools import lru_cache

from authentication.models import User
from src.common.providers.blueprint_provider import default_blueprint_provider
from storage.data_source_interface import DataSource
from src.storage.internal.data_source_repository import DataSourceRepository


# This is needed to be able to cache 'get_data_source', as 'get_blueprint' is not hashable
class GetDataSourceCached:
    def __init__(self, blueprint_provider):
        self.get_blueprint = blueprint_provider

    @lru_cache(maxsize=128)  # noqa B019
    def get(self, data_source_id: str, user: User) -> DataSource:
        return DataSourceRepository(user, self.get_blueprint).get(data_source_id)


get_data_source_cached = GetDataSourceCached(default_blueprint_provider).get
