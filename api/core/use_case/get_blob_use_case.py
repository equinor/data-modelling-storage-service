from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source


class GetBlobUseCase(uc.UseCase):
    def process_request(self, request_object):
        data_source_id: str = request_object["data_source"]
        blob_id: str = request_object["blob_id"]

        data_source = get_data_source(data_source_id)
        blob = data_source.get_blob(blob_id)

        return res.ResponseSuccess(blob)
