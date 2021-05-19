from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService


class DeleteReferenceRequest(DataSource):
    document_id: str
    attribute: str


class DeleteReferenceUseCase(UseCase):
    def process_request(self, req: DeleteReferenceRequest):
        document_service = DocumentService()
        document = document_service.remove_reference(
            data_source_id=req.data_source_id, document_id=req.document_id, attribute_path=req.attribute,
        )
        return ResponseSuccess(document)
