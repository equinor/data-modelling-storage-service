from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Json
from starlette.responses import JSONResponse

from restful.request_types.shared import EntityName
from restful.status_codes import STATUS_CODES
from storage.internal.data_source_repository import get_data_source
from use_case.add_document_to_path_use_case import AddDocumentToPathRequest, AddDocumentToPathUseCase
from use_case.add_file_use_case import AddFileUseCase
from use_case.add_raw import AddRawRequest, AddRawUseCase
from use_case.add_root_package_use_case import AddRootPackageRequest, AddRootPackageUseCase
from use_case.move_file_use_case import MoveFileUseCase, MoveRequest
from use_case.remove_by_path_use_case import RemoveByPathRequest, RemoveByPathUseCase
from use_case.remove_use_case import RemoveRequest, RemoveUseCase
from use_case.rename_file_use_case import RenameRequest, RenameUseCase

router = APIRouter()


@router.post("/explorer/{data_source_id}/add-to-path", operation_id="explorer_add_to_path")
def add_to_path(
    data_source_id: str,
    document: Json = Form(...),
    directory: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
):
    """
    Same as 'add_to_parent', but reference parent by path instead of ID. Also supports files.
    """
    use_case = AddDocumentToPathUseCase()
    response = use_case.execute(
        AddDocumentToPathRequest(data_source_id=data_source_id, document=document, directory=directory, files=files)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-package", operation_id="explorer_add_package")
def add_package(data_source_id: str, name: EntityName):
    """Add a RootPackage to the data source"""
    use_case = AddRootPackageUseCase()
    response = use_case.execute(AddRootPackageRequest(data_source_id=data_source_id, name=name.name))

    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


# TODO: Create test for this
@router.post("/explorer/{data_source_id}/add-raw", operation_id="explorer_add_raw")
def add_raw(data_source_id: str, document: dict):
    """
    NOTE: The 'add-document' operation is to be preferred.
    This is mainly for bootstrapping and imports.
    Blueprint need not exist, and so there is no validation.
    Posted document must be a valid Entity ('name' and 'type' required).
    """
    use_case = AddRawUseCase()
    response = use_case.execute(AddRawRequest(data_source_id=data_source_id, document=document))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


# TODO: Create test for this
# TODO: DataSource is not needed in the path, as it's contained in the source and dest parameters
@router.post("/explorer/{data_source_id}/move", operation_id="explorer_move")
def move(data_source_id: str, request_data: MoveRequest):  # noqa: E501
    use_case = MoveFileUseCase(get_repository=get_data_source)
    response = use_case.execute(request_data)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.delete("/explorer/{data_source_id}/{dotted_id}", operation_id="explorer_remove")
def remove(data_source_id: str, dotted_id: str):
    use_case = RemoveUseCase()
    response = use_case.execute(RemoveRequest(data_source_id=data_source_id, documentId=dotted_id))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/remove-by-path", operation_id="explorer_remove_by_path")
def remove_by_path(data_source_id: str, request: RemoveByPathRequest):  # noqa: E501
    request.data_source_id = data_source_id
    use_case = RemoveByPathUseCase()
    response = use_case.execute(request)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/explorer/{data_source_id}/rename", operation_id="explorer_rename")
def rename(data_source_id: str, request_data: RenameRequest):  # noqa: E501
    request_data.data_source_id = data_source_id
    use_case = RenameUseCase()
    response = use_case.execute(request_data)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/{dotted_id}", operation_id="explorer_add")
def add_by_parent_id(data_source_id: str, dotted_id: str, data: dict):
    """
    Add a new document into an existing one. Must match it's parents attribute type.
    Select parent with format 'document-id.attribute.attribute'
    """
    use_case = AddFileUseCase()
    response = use_case.execute({"absolute_ref": f"{data_source_id}/{dotted_id}", "data": data})
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
