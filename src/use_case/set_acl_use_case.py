from authentication.access_control import ACL
from restful.request_types.shared import DataSource
from restful.response_object import ResponseSuccess
from restful.use_case import UseCase
from services.document_service import DocumentService


class SetACLRequest(DataSource):
    document_id: str
    acl: ACL


class SetACLUseCase(UseCase):
    def process_request(self, req: SetACLRequest):
        document_service = DocumentService()
        document_service.set_acl(data_source_id=req.data_source_id, document_id=req.document_id, acl=req.acl)
        return ResponseSuccess("OK")
