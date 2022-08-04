from restful import use_case
from restful.request_types.shared import DataSource


class GetDataSourceUseCase(use_case.UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, data_source: DataSource):
        data_source = self.data_source_repository.get(data_source.data_source_id)
        return {"name": data_source.name, "id": data_source.name}
