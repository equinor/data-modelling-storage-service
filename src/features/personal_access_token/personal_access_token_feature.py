from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.access_control import AccessLevel
from authentication.authentication import auth_with_jwt
from authentication.models import PATData, User
from authentication.personal_access_token import create_personal_access_token
from common.responses import create_response, responses
from storage.internal.personal_access_tokens import delete_pat, get_users_pats

router = APIRouter(tags=["default", "personal_access_token"], prefix="/token")


@router.post("", operation_id="token_create", response_model=str, responses=responses)
@create_response(PlainTextResponse)
async def new_personal_access_token(
    scope: AccessLevel = AccessLevel.WRITE,
    time_to_live: int = int(timedelta(days=30).total_seconds()),
    user: User = Depends(auth_with_jwt),
) -> str:
    """Create a Personal Access Token (PAT).

    This endpoint creates a PAT token for the currently logged in user, stores it in the database and returns it to the user.

    Args:
        scope (WRITE | READ | NONE): Access level for the PAT.
        time_to_live (int): Optional parameter specifying the lifespan of the PAT in seconds. Default lifespan is 30 days.

    Returns:
        str: The generated PAT token
    """
    return create_personal_access_token(user, scope, time_to_live)


@router.delete("/{token_id}", operation_id="token_delete", response_model=str, responses=responses)
@create_response(PlainTextResponse)
async def revoke_personal_access_token(token_id: str, user: User = Depends(auth_with_jwt)) -> str:
    """Revoke a Personal Access Token (PAT).

    This endpoint revokes a PAT token so that it is invalid and can no longer be used to gain access.

    Args:
        token_id (str): The ID of the token to be revoked.

    Returns:
        str: A string with the message "OK" when the token has been revoked.
    """
    delete_pat(token_id, user)
    return "OK"


@router.get("", operation_id="token_list_all", response_model=list[PATData], responses=responses)
@create_response(JSONResponse)
async def list_all_pats(user: User = Depends(auth_with_jwt)) -> list[PATData]:
    """Get All Personal Access Tokens for the Current User.

    Get a list of all personal access tokens (PATs) for the currently logged in user.

    Args:
        user (User): The authenticated user accessing the endpoint.

    Returns:
        list: A list of all personal access tokens for the currently logged in user.
    """
    return get_users_pats(user)
