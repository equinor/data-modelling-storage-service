from fastapi import APIRouter, Depends

from authentication.authentication import get_current_user
from authentication.models import User

router = APIRouter()


@router.get("/whoami", operation_id="whoami")
async def get_information_on_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user
