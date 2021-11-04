from fastapi import APIRouter, File, UploadFile, Depends
from starlette.responses import FileResponse, JSONResponse, Response

from authentication.authentication import get_current_user
from domain_classes.user import User
from restful.status_codes import STATUS_CODES
from storage.internal.data_source_repository import get_data_source
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
def get_by_id(data_source_id: str, blob_id: str, user: User = Depends(get_current_user)):
    use_case = GetBlobUseCase(user)
    response = use_case.execute(GetBlobRequest(data_source_id=data_source_id, blob_id=blob_id))
    if not response.type == "SUCCESS":
        return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
    # Response is string encoded 'bytes'
    return Response(response.value)


# For the OpenAPI generation, we specify response and response class.
@router.put("/blobs/{data_source_id}/{blob_id}", operation_id="blob_upload")
def upload(data_source_id: str, blob_id: str, file: UploadFile = File(...), user: User = Depends(get_current_user)):
    data_source = get_data_source(data_source_id, user)
    data_source.update_blob(blob_id, file.file)
    return Response("OK")
