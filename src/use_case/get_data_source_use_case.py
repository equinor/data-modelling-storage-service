from restful import response_object, use_case
from restful.request_types.shared import DataSource


class GetDataSourceUseCase(use_case.UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, data_source_id: DataSource):
        data_sources = self.data_source_repository.get(data_source_id.data_source_id)
        return response_object.ResponseSuccess(data_sources)
