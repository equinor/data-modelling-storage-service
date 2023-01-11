from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import FileResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.get_blob_use_case import get_blob_use_case
from .use_cases.upload_blob_use_case import upload_blob_use_case

router = APIRouter(tags=["default", "blob"], prefix="/blobs")


# For the OpenAPI generation, we specify response and response class.
@router.get(
    "/{data_source_id}/{blob_id}",
    operation_id="blob_get_by_id",
    responses={
        **responses,
        200: {"content": {"application/octet-stream": {"schema": {"type": "string", "format": "binary"}}}},
    },
    response_class=FileResponse,
)
@create_response(PlainTextResponse)
def get_by_id(data_source_id: str, blob_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Get blob from id.
    A blob (binary large object) can be anything from video to text file.
    """
    return get_blob_use_case(user=user, data_source_id=data_source_id, blob_id=blob_id)


@router.put("/{data_source_id}/{blob_id}", operation_id="blob_upload", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def upload(
    data_source_id: str,
    blob_id: str,
    file: UploadFile = File(...),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Upload a new blob.
    A blob (binary large object) can be anything from video to text file.
    """
    return upload_blob_use_case(user=user, data_source_id=data_source_id, blob_id=blob_id, file=file)
