from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import Json

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.add_file_use_case import add_file_use_case

router = APIRouter(tags=["default", "file"], prefix="/files")


@router.post("/{data_source_id}", operation_id="file_upload", response_model=dict, responses=responses)
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
        data_source_id (str):
        data (dict with a "file_id" attribute): A dict containing data source ID to be used for the file entity that will be created.
        user (User): The authenticated user accessing the endpoint.

    Returns:
        dict: The file entity that was created to contain the file.
    """
    return await add_file_use_case(data_source_id, data["file_id"], file, user)
