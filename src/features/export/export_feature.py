from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import responses

from .use_cases.export_use_case import export_use_case

router = APIRouter(tags=["default", "export"], prefix="/export")


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
