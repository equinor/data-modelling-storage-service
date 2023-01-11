from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import ACL, User
from common.responses import create_response, responses

from .use_cases.get_acl_use_case import get_acl_use_case
from .use_cases.set_acl_use_case import set_acl_use_case

router = APIRouter(tags=["default", "access_control"], prefix="/acl")


@router.put("/{data_source_id}/{document_id}", operation_id="set_acl", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def set_acl(
    data_source_id: str, document_id: str, acl: ACL, recursively: bool = True, user: User = Depends(auth_w_jwt_or_pat)
):
    """Update access control list (ACL) for a document.

    The ACL determines which access a given user has for a document (Read, Write or None).
    """
    return set_acl_use_case(
        user=user, data_source_id=data_source_id, document_id=document_id, acl=acl, recursively=recursively
    )


@router.get("/{data_source_id}/{document_id}", operation_id="get_acl", response_model=ACL, responses=responses)
@create_response(JSONResponse)
def get_acl(data_source_id: str, document_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """get access control list (ACL) for a document.

    The ACL determines which access a given user has for a document (Read, Write or None).
    """
    return get_acl_use_case(user=user, data_source_id=data_source_id, document_id=document_id).dict()
