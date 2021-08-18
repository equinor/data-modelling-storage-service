from fastapi import APIRouter
from starlette.responses import JSONResponse

from authentication.access_control import ACL
from restful.status_codes import STATUS_CODES
from use_case.get_acl_use_case import GetACLRequest, GetACLUseCase
from use_case.set_acl_use_case import SetACLRequest, SetACLUseCase

router = APIRouter()


# TODO: Should this be able to set ACL recursively? Probably...
@router.put("/acl/{data_source_id}/{document_id}", operation_id="set_acl", response_model=dict)
def set_acl(data_source_id: str, document_id: str, acl: ACL):
    use_case = SetACLUseCase()
    response = use_case.execute(SetACLRequest(data_source_id=data_source_id, document_id=document_id, acl=acl))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get("/acl/{data_source_id}/{document_id}", operation_id="get_acl", response_model=ACL)
def get_acl(data_source_id: str, document_id: str):
    use_case = GetACLUseCase()
    response = use_case.execute(GetACLRequest(data_source_id=data_source_id, document_id=document_id))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
