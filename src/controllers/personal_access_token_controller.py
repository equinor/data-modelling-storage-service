from datetime import timedelta

from fastapi import APIRouter, Depends

from authentication.access_control import AccessLevel
from authentication.authentication import auth_with_jwt
from authentication.models import PATData, User
from authentication.personal_access_token import create_personal_access_token
from storage.internal.personal_access_tokens import delete_pat, get_users_pats

router = APIRouter()


@router.post("/token", operation_id="token_create")
async def new_personal_access_token(
    scope: AccessLevel = AccessLevel.WRITE,
    time_to_live: int = timedelta(days=30).total_seconds(),
    user: User = Depends(auth_with_jwt),
) -> str:
    return create_personal_access_token(user, scope, time_to_live)


@router.delete("/token/{token_id}", operation_id="token_delete")
async def revoke_personal_access_token(token_id: str, user: User = Depends(auth_with_jwt)) -> str:
    delete_pat(token_id, user)
    return "OK"


@router.get("/token", operation_id="token_list_all")
async def list_all_pats(user: User = Depends(auth_with_jwt)) -> list[PATData]:
    return get_users_pats(user)
