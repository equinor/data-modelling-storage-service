import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.responses import FileResponse, JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from domain_classes.dependency import Dependency
from features.export.use_cases.export_meta_use_case import export_meta_use_case
from features.export.use_cases.export_use_case import export_use_case

router = APIRouter(tags=["default", "export"], prefix="/export")


class ExportMetaResponse(BaseModel):
    type: str = "CORE:Meta"
    version: str = "0.0.0"
    dependencies: List[Dependency] = []


@router.get(
    "/meta/{path_address:path}",
    operation_id="export-meta",
    response_class=JSONResponse,
    response_model=ExportMetaResponse,
    responses={**responses, 200: {"content": {"application/json": {}}}},
)
@create_response(JSONResponse)
def export_meta(path_address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Get Meta Information About a Document

    This endpoint returns meta information about a document provided document id and data source id in which it is
    located.
    For more information about the meta-object, see [the docs](https://equinor.github.io/dm-docs/docs/concepts/meta)

    Args:
    - path_address (str): Address of the object for which to get the meta-information.
        - Example: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY (PROTOCOL is optional, and the default is dmss.)
    - user (User): The authenticated user accessing the endpoint.

    Returns:
    - dict: A dictionary containing the meta information for the object.
    """
    return ExportMetaResponse(**export_meta_use_case(user=user, path_address=path_address)).dict()


@router.get(
    "/{path_address:path}",
    operation_id="export",
    response_class=FileResponse,
    responses={**responses, 200: {"content": {"application/zip": {}}}},
)
def export(path_address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Download a zip-folder Containing One or More Documents as JSON Files.

    This endpoint creates a zip-folder with the contents of the document and it's children.

    Args:
    - path_address: Address to the entity or package that should be exported.
      - Example: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY (PROTOCOL is optional, and the default is dmss.)
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - FileResponse: A FileResponse containing the zip file.
    """
    # TODO add proper error handling. The create_response() wrapper does not work with FileResponse.
    memory_file_path = export_use_case(user=user, address=path_address)
    directory_to_remove = Path(memory_file_path).parent
    response = FileResponse(
        memory_file_path, media_type="application/zip", background=BackgroundTask(shutil.rmtree, directory_to_remove)
    )
    response.headers["Content-Disposition"] = "attachment; filename=dmt-export.zip"

    return response
