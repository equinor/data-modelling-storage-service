from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from use_case.export_use_case import ExportUseCase

router = APIRouter()
responses = {200: {"content": {"application/zip": {}}}}


@router.get(
    "/export/{absolute_document_ref:path}", operation_id="export", response_class=FileResponse, responses=responses
)
def export(absolute_document_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Download a zip-folder of the requested root package
    """
    use_case = ExportUseCase(user)
    return use_case.execute(absolute_document_ref)
