from fastapi import APIRouter
from starlette.responses import FileResponse, Response

from restful.status_codes import STATUS_CODES
from use_case.get_blob_use_case import GetBlobRequest, GetBlobUseCase

router = APIRouter()

responses = {200: {"content": {"application/octet-stream": {"schema": {"type": "string", "format": "binary"}}}}}


# For the OpenAPI generation, we specify response and response class.
@router.get(
    "/blobs/{data_source_id}/{blob_id}",
    operation_id="blob_get_by_id",
    responses=responses,
    response_class=FileResponse,
)
def get_by_id(data_source_id: str, blob_id: str):
    use_case = GetBlobUseCase()
    response = use_case.execute(GetBlobRequest(data_source_id=data_source_id, blob_id=blob_id))
    if not response.type == "SUCCESS":
        return Response(response.value, status_code=STATUS_CODES[response.type])
    # Response is string encoded 'bytes'
    return Response(response.value)
