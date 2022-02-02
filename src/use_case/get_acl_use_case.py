from authentication.models import ACL, User
from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService


class GetACLRequest(DataSource):
    document_id: str


class GetACLUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: GetACLRequest):
        document_service = DocumentService(user=self.user)
        acl: ACL = document_service.get_acl(data_source_id=req.data_source_id, document_id=req.document_id)
        return ResponseSuccess(acl.dict())
