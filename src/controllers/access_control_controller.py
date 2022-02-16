from fastapi import APIRouter, Depends

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import ACL, User
from use_case.get_acl_use_case import GetACLRequest, GetACLUseCase
from use_case.set_acl_use_case import SetACLRequest, SetACLUseCase

router = APIRouter()


@router.put("/acl/{data_source_id}/{document_id}", operation_id="set_acl", response_model=str)
def set_acl(
    data_source_id: str, document_id: str, acl: ACL, recursively: bool = True, user: User = Depends(auth_w_jwt_or_pat)
):
    use_case = SetACLUseCase(user)
    return use_case.execute(
        SetACLRequest(data_source_id=data_source_id, document_id=document_id, acl=acl, recursively=recursively)
    )


@router.get("/acl/{data_source_id}/{document_id}", operation_id="get_acl", response_model=ACL)
def get_acl(data_source_id: str, document_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    use_case = GetACLUseCase(user)
    return use_case.execute(GetACLRequest(data_source_id=data_source_id, document_id=document_id))
