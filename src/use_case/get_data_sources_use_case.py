from restful import response_object
from restful.use_case import UseCase


class GetDataSourcesUseCase(UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, request_object=None):
        data_sources = self.data_source_repository.list()
        return response_object.ResponseSuccess(data_sources)
