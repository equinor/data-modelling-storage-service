from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import FileResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
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
def get_by_id(data_source_id: str, blob_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    use_case = GetBlobUseCase(user)
    return use_case.execute(GetBlobRequest(data_source_id=data_source_id, blob_id=blob_id))


# For the OpenAPI generation, we specify response and response class.
@router.put("/blobs/{data_source_id}/{blob_id}", operation_id="blob_upload")
def upload(data_source_id: str, blob_id: str, file: UploadFile = File(...), user: User = Depends(auth_w_jwt_or_pat)):
    data_source = get_data_source(data_source_id, user)
    data_source.update_blob(blob_id, file.file)
    return PlainTextResponse("OK")
