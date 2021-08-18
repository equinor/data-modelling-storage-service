from fastapi import APIRouter
from authentication import authentication

router = APIRouter()


@router.get("/whoami", operation_id="whoami")
async def get_information_on_authenticated_user():
    return authentication.user_context
