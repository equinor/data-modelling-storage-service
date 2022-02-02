from authentication.models import User
from restful.request_types.shared import DataSource, Reference
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService


class InsertReferenceRequest(DataSource):
    document_id: str
    reference: Reference
    attribute: str


class InsertReferenceUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: InsertReferenceRequest):
        document_service = DocumentService(user=self.user)
        document = document_service.insert_reference(
            data_source_id=req.data_source_id,
            document_id=req.document_id,
            reference=req.reference,
            attribute_path=req.attribute,
        )
        return ResponseSuccess(document)
