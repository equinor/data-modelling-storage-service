from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import Json

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.add_file_use_case import AddFileResponseModel, add_file_use_case

router = APIRouter(tags=["default", "file"], prefix="/files")


@router.post(
    "/{data_source_id}",
    operation_id="file_upload",
    response_model=dict,
    responses=responses,
)
@create_response(JSONResponse)
async def upload_file(
    data_source_id: str,
    data: Json = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Upload a New Binary File

    This endpoint uploads a new file and creates a file entity with the uploaded binary data as content.

    Args:
    - data_source_id (str): ID of the data source to which the file should be uploaded.
    - data (dict with a "file_id" attribute): A dict containing data source ID to be used for the file entity that will be created.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: The file entity that was created to contain the file.
    """
    return await add_file_use_case(data_source_id, data["file_id"], file, user)


@router.post(
    "/{data_source_id}/multiple",
    operation_id="file_uploads",
    response_model=list[AddFileResponseModel],
    responses=responses,
)
@create_response(JSONResponse)
async def upload_files(
    data_source_id: str,
    data: Json = Form(...),
    files: list[UploadFile] = File(...),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Upload Binary Files

    This endpoint uploads files and creates a file entity with the uploaded binary data as content.

    Args:
    - data_source_id (str): ID of the data source to which the file should be uploaded.
    - data (dict with a "file_ids" attribute): A dict containing data source IDs to be used for the file entities that will be created.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - list[dict]: The file entities that was created to contain the files.
    """
    return [
        await add_file_use_case(data_source_id, data["file_ids"][index], files[index], user)
        for index in range(len(files))
    ]
