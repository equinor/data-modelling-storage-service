from fastapi import APIRouter, Depends

from authentication.authentication import get_current_user
from authentication.personal_access_token import create_personal_access_token
from domain_classes.user import User

router = APIRouter()


@router.get("/token", operation_id="token_get")
async def get_personal_access_token(user: User = Depends(get_current_user)):
    return create_personal_access_token(user)
