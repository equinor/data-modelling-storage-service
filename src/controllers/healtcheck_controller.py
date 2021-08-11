from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", operation_id="healthcheck")
async def healthcheck():
    return "OK"
