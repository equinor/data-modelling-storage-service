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
    """Get the Health Status Of the Service.

    This endpoint can be used to check the health status of the service.
    It always returns a 200 OK response to indicate that the service is up and running.

    Args:
        user (User): The authenticated user accessing the endpoint.

    Returns:
        string: A string indicating the health status.
            "OK"
    """
    return "OK"
