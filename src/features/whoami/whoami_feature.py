from fastapi import APIRouter, Depends

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import responses

router = APIRouter(tags=["default", "whoami"], prefix="/whoami")


@router.get("", operation_id="whoami", responses=responses)
async def get_information_on_authenticated_user(user: User = Depends(auth_w_jwt_or_pat)):
    return user
