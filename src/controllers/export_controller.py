from fastapi import APIRouter, Depends
from starlette.responses import FileResponse, JSONResponse

from authentication.authentication import get_current_user
from domain_classes.user import User
from restful.status_codes import STATUS_CODES
from use_case.export_use_case import ExportUseCase

router = APIRouter()
responses = {200: {"content": {"application/zip": {}}}}


@router.get(
    "/export/{absolute_document_ref:path}", operation_id="export", response_class=FileResponse, responses=responses
)
def export(absolute_document_ref: str, user: User = Depends(get_current_user)):
    """
    Download a zip-folder of the requested root package
    """
    use_case = ExportUseCase(user)
    response = use_case.execute(absolute_document_ref)

    if response.type == response.type == "SUCCESS":
        response = FileResponse(response.value, media_type="application/zip")
        response.headers["Content-Disposition"] = "attachment; filename=dmt-export.zip"
        return response
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
