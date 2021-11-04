from fastapi import APIRouter, Depends
from authentication.authentication import get_current_user
from domain_classes.user import User

router = APIRouter()


@router.get("/whoami", operation_id="whoami")
async def get_information_on_authenticated_user(user: User = Depends(get_current_user)):
    return user
