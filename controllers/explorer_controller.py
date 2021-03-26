from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from starlette.responses import JSONResponse

from api.core.storage.internal.data_source_repository import get_data_source
from api.core.use_case.add_document_to_path_use_case import AddDocumentToPathRequestObject, AddDocumentToPathUseCase
from api.core.use_case.add_document_use_case import AddDocumentRequestObject, AddDocumentUseCase
from api.core.use_case.add_file_use_case import AddFileRequestObject, AddFileUseCase
from api.core.use_case.add_raw import AddRawRequestObject, AddRawUseCase
from api.core.use_case.add_root_package_use_case import AddRootPackageRequestObject, AddRootPackageUseCase
from api.core.use_case.move_file_use_case import MoveFileRequestObject, MoveFileUseCase
from api.core.use_case.remove_by_path_use_case import RemoveByPathRequestObject, RemoveByPathUseCase
from api.core.use_case.remove_use_case import RemoveFileRequestObject, RemoveUseCase
from api.core.use_case.rename_file_use_case import RenameRequestObject, RenameUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.post("/explorer/{data_source_id}/add-document")
def add_document(data_source_id: str, request_data: dict):
    request_data["data_source_id"] = data_source_id
    use_case = AddDocumentUseCase()
    request_object = AddDocumentRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-to-parent")
def add_to_parent(data_source_id: str, request_data: dict):
    request_data["data_source_id"] = data_source_id
    use_case = AddFileUseCase()
    request_object = AddFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-to-path")
def add_to_path(data_source_id: str, document: str = Form(...), directory: str = Form(...),
                files: Optional[List[UploadFile]] = File(None)):
    body = {}
    body["data_source_id"] = data_source_id
    body["files"] = {f.filename: f.file for f in files}
    body["document"] = document
    body["directory"] = directory
    use_case = AddDocumentToPathUseCase()
    request_object = AddDocumentToPathRequestObject.from_dict(body)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-package")
def add_package(data_source_id: str, request_data: dict):
    request_data["data_source_id"] = data_source_id
    use_case = AddRootPackageUseCase()
    request_object = AddRootPackageRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)

    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-raw")
def add_raw(data_source_id: str, request_data: dict):
    request_data["data_source_id"] = data_source_id
    use_case = AddRawUseCase()
    request_object = AddRawRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/move")
def move(request_data: dict):  # noqa: E501
    use_case = MoveFileUseCase(get_repository=get_data_source)
    request_object = MoveFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/remove")
def remove(data_source_id: str, request_data: dict):  # noqa: E501
    request_data["data_source_id"] = data_source_id
    use_case = RemoveUseCase()
    request_object = RemoveFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/remove-by-path")
def remove_by_path(data_source_id: str, request_data: dict):  # noqa: E501
    request_data["data_source_id"] = data_source_id
    use_case = RemoveByPathUseCase()
    request_object = RemoveByPathRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/explorer/{data_source_id}/rename")
def rename(data_source_id: str, request_data: dict):  # noqa: E501
    request_data["data_source_id"] = data_source_id
    use_case = RenameUseCase()
    request_object = RenameRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
