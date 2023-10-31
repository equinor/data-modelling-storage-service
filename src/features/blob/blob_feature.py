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

    A blob file is a binary object, which can be any kind of data object.

    Args:
    - data_source_id (str): The ID of the data source in which to find the blob.
    - blob_id (str): The ID of the requested blob.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - Filestream: The requested blob.
    """
    return get_blob_use_case(user=user, data_source_id=data_source_id, blob_id=blob_id)


@router.put(
    "/{data_source_id}/{blob_id}",
    operation_id="blob_upload",
    response_model=str,
    responses=responses,
)
@create_response(PlainTextResponse)
def upload(
    data_source_id: str,
    blob_id: str,
    file: UploadFile = File(...),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Upload a new blob or modify an existings blob.

    A blob (binary large object) can be anything from video to text file.
    If you give an ID to a blob that already exists, the old blob will be updated in place.

    Args:
    - data_source_id (str): The ID of the data source in which to store the blob.
    - blob_id (str): The ID that the blob should be stored under.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - str: OK (200)
    """
    return upload_blob_use_case(user=user, data_source_id=data_source_id, blob_id=blob_id, file=file)
