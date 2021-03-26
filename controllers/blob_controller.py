from fastapi import APIRouter
from starlette.responses import JSONResponse, StreamingResponse

from api.core.use_case.get_blob_use_case import GetBlobUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.get("/blobs/{data_source_id}/{blob_id}")
def get_blob_by_id(data_source_id: str, blob_id: str):
    use_case = GetBlobUseCase()
    response = use_case.execute({"data_source": data_source_id, "blob_id": blob_id})
    if not response.type == "SUCCESS":
        return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
    return StreamingResponse(response.value, media_type="application/octet-stream")
