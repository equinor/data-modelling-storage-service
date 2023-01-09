from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from common.responses import responses

router = APIRouter(tags=["default", "health_check"], prefix="/healthcheck")


@router.get(
    "",
    responses={**responses, 200: {"model": str, "content": {"text/plain": {"example": "OK"}}}},
    response_class=PlainTextResponse,
)
async def get():
    """Test if DMSS is running."""
    return "OK"
