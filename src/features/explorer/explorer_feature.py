from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.rename_file_use_case import rename_use_case

router = APIRouter(tags=["default", "explorer"], prefix="/explorer")


# TODO: Create test for this
# TODO: DataSource is not needed in the path, as it's contained in the source and dest parameters
@router.post("/{data_source_id}/move", operation_id="explorer_move", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def move(request_data, data_source_id: str, user: User = Depends(auth_w_jwt_or_pat)):  # noqa: E501
    raise NotImplementedError


@router.put("/{data_source_id}/rename", operation_id="explorer_rename", response_model=dict, responses=responses)
@create_response(JSONResponse)
def rename(
    data_source_id: str,
    document_id: str,
    parent_id: str,
    user: User = Depends(auth_w_jwt_or_pat),
):  # noqa: E501
    return rename_use_case(user=user, data_source_id=data_source_id, document_id=document_id, parent_id=parent_id)
