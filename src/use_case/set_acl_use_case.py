from authentication.access_control import ACL
from domain_classes.user import User
from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService


class SetACLRequest(DataSource):
    document_id: str
    acl: ACL
    recursively: bool


class SetACLUseCase(UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: SetACLRequest):
        document_service = DocumentService(user=self.user)
        document_service.set_acl(
            data_source_id=req.data_source_id, document_id=req.document_id, acl=req.acl, recursively=req.recursively
        )
        return ResponseSuccess("OK")
