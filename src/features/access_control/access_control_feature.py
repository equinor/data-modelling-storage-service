from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import ACL, User
from .use_cases.get_acl_use_case import get_acl_use_case
from common.responses import create_response
from restful.request_types.shared import data_source_id_query
from .use_cases.set_acl_use_case import set_acl_use_case

router = APIRouter(tags=["default", "access_control"], prefix="/acl")


@router.put("/{data_source_id}/{document_id}", operation_id="set_acl", response_model=str)
@create_response(PlainTextResponse)
def set_acl(
    document_id: str,
    acl: ACL,
    recursively: bool = True,
    user: User = Depends(auth_w_jwt_or_pat),
    data_source_id: str = data_source_id_query,
):
    return set_acl_use_case(
        user=user, data_source_id=data_source_id, document_id=document_id, acl=acl, recursively=recursively
    )


@router.get("/{data_source_id}/{document_id}", operation_id="get_acl", response_model=ACL)
@create_response(JSONResponse)
def get_acl(document_id: str, data_source_id: str = data_source_id_query, user: User = Depends(auth_w_jwt_or_pat)):
    return get_acl_use_case(user=user, data_source_id=data_source_id, document_id=document_id).dict()
