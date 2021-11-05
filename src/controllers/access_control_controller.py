from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from authentication.access_control import ACL
from authentication.authentication import get_current_user
from domain_classes.user import User
from restful.status_codes import STATUS_CODES
from use_case.get_acl_use_case import GetACLRequest, GetACLUseCase
from use_case.set_acl_use_case import SetACLRequest, SetACLUseCase

router = APIRouter()


@router.put("/acl/{data_source_id}/{document_id}", operation_id="set_acl", response_model=dict)
def set_acl(
    data_source_id: str, document_id: str, acl: ACL, recursively: bool = True, user: User = Depends(get_current_user)
):
    use_case = SetACLUseCase(user)
    response = use_case.execute(
        SetACLRequest(data_source_id=data_source_id, document_id=document_id, acl=acl, recursively=recursively)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get("/acl/{data_source_id}/{document_id}", operation_id="get_acl", response_model=ACL)
def get_acl(data_source_id: str, document_id: str, user: User = Depends(get_current_user)):
    use_case = GetACLUseCase(user)
    response = use_case.execute(GetACLRequest(data_source_id=data_source_id, document_id=document_id))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
