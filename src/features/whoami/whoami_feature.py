from fastapi import APIRouter, Depends

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import responses

router = APIRouter(tags=["default", "whoami"], prefix="/whoami")


@router.get("", operation_id="whoami", responses=responses)
async def get_information_on_authenticated_user(user: User = Depends(auth_w_jwt_or_pat)):
    """Get information about the user who sent the request.

    If no user is authenticated, a default "nologin" user is returned.
    This endpoint always responds with a status code of 200 (OK).

    Args:
        user (User): The authenticated user accessing the endpoint.

    Returns:
        dict: A dictionary containing information about the user who sent the request.
        Example:
        {
            "user_id": "1234",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
            "roles": [],
            "scope": "WRITE"¯
        }
    """
    return user
