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
    "/meta/{address:path}",
    operation_id="export-meta",
    response_class=JSONResponse,
    responses={**responses, 200: {"content": {"application/json": {}}}},
)
@create_response(JSONResponse)
def export_meta(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Export only the metadata of an entity.
    An entities metadata is concatenated from the "top down". Inheriting parents meta, and overriding for any
    specified further down.

    If no metadata is defined anywhere in the tree, an empty object is returned.

    - **address**:
      - By path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY

      The PROTOCOL is optional, and the default is dmss.
    """
    return ExportMetaResponse(**export_meta_use_case(user=user, address=address)).dict()


@router.get(
    "/{address:path}",
    operation_id="export",
    response_class=FileResponse,
    responses={**responses, 200: {"content": {"application/zip": {}}}},
)
def export(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Download a zip-folder with one or more documents as json file(s).

    - **address**:
      - By path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY

      The PROTOCOL is optional, and the default is dmss.
    """
    # TODO add proper error handling. The create_response() wrapper does not work with FileResponse.
    memory_file_path = export_use_case(user=user, document_address=address)
    directory_to_remove = Path(memory_file_path).parent
    response = FileResponse(
        memory_file_path, media_type="application/zip", background=BackgroundTask(shutil.rmtree, directory_to_remove)
    )
    response.headers["Content-Disposition"] = "attachment; filename=dmt-export.zip"

    return response
