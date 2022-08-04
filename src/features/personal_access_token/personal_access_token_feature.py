from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from common.responses import create_response

from authentication.access_control import AccessLevel
from authentication.authentication import auth_with_jwt
from authentication.models import PATData, User
from authentication.personal_access_token import create_personal_access_token
from storage.internal.personal_access_tokens import delete_pat, get_users_pats

router = APIRouter(tags=["personal_access_token"], prefix="/token")


@router.post("", operation_id="token_create", response_model=str)
@create_response(PlainTextResponse)
async def new_personal_access_token(
    scope: AccessLevel = AccessLevel.WRITE,
    time_to_live: int = timedelta(days=30).total_seconds(),
    user: User = Depends(auth_with_jwt),
) -> str:
    return create_personal_access_token(user, scope, time_to_live)


@router.delete("/{token_id}", operation_id="token_delete", response_model=str)
@create_response(PlainTextResponse)
async def revoke_personal_access_token(token_id: str, user: User = Depends(auth_with_jwt)) -> str:
    delete_pat(token_id, user)
    return "OK"


@router.get("", operation_id="token_list_all", response_model=list[PATData])
@create_response(JSONResponse)
async def list_all_pats(user: User = Depends(auth_with_jwt)) -> list[PATData]:
    return get_users_pats(user)
