from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
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
    "/meta/{absolute_document_ref:path}",
    operation_id="export-meta",
    response_class=JSONResponse,
    responses={**responses, 200: {"content": {"application/json": {}}}},
)
@create_response(JSONResponse)
def export_meta(absolute_document_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Export only the metadata of an entity.
    Entities must be specified on the format 'DATASOURCE/PACKAGE/{ENTITY.name/ENTITY._id}
    An entities metadata is concatenated from the "top down". Inheriting parents meta, and overriding for any
    specified further down.

    If no metadata is defined anywhere in the tree, an empty object is returned.
    """
    return ExportMetaResponse(**export_meta_use_case(user=user, document_reference=absolute_document_ref)).dict()


# TODO use create_response declarator. Must be able to handle FileResponse.
@router.get(
    "/{absolute_document_ref:path}",
    operation_id="export",
    response_class=FileResponse,
    responses={**responses, 200: {"content": {"application/zip": {}}}},
)
def export(absolute_document_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Download a zip-folder of the requested root package
    """
    memory_file = export_use_case(user=user, document_reference=absolute_document_ref)
    response = FileResponse(memory_file, media_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=dmt-export.zip"

    return response
