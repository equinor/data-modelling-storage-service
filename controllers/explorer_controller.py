from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Json
from starlette.responses import JSONResponse

from api.core.storage.internal.data_source_repository import get_data_source
from api.core.use_case.add_document_to_path_use_case import AddDocumentToPathRequest, AddDocumentToPathUseCase
from api.core.use_case.add_document_use_case import AddDocumentRequest, AddDocumentUseCase
from api.core.use_case.add_file_use_case import AddFileUseCase, AddToParentRequest
from api.core.use_case.add_raw import AddRawUseCase
from api.core.use_case.add_root_package_use_case import AddRootPackageRequest, AddRootPackageUseCase
from api.core.use_case.move_file_use_case import MoveFileUseCase, MoveRequest
from api.core.use_case.remove_by_path_use_case import RemoveByPathRequest, RemoveByPathUseCase
from api.core.use_case.remove_use_case import RemoveRequest, RemoveUseCase
from api.core.use_case.rename_file_use_case import RenameRequest, RenameUseCase
from api.request_types.shared import EntityName, NamedEntity
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.post("/explorer/{data_source_id}/add-document")
def add_document(data_source_id: str, document: NamedEntity):
    use_case = AddDocumentUseCase()
    response = use_case.execute(AddDocumentRequest(data_source_id=data_source_id, data=document))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-to-parent")
def add_to_parent(data_source_id: str, request_data: AddToParentRequest):
    """
    Add a new document into an existing one. Must match it's parents attribute type
    """
    use_case = AddFileUseCase()
    request_data.data_source_id = data_source_id
    response = use_case.execute(request_data)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/add-to-path")
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


@router.post("/explorer/{data_source_id}/add-package")
def add_package(data_source_id: str, name: EntityName):
    use_case = AddRootPackageUseCase()
    response = use_case.execute(AddRootPackageRequest(data_source_id=data_source_id, name=name.name))

    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


# TODO: Create test for this
@router.post("/explorer/{data_source_id}/add-raw")
def add_raw(data_source_id: str, document: NamedEntity):
    use_case = AddRawUseCase()
    response = use_case.execute({"data_source_id": data_source_id, "document": document})
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


# TODO: Create test for this
# TODO: DataSource is not needed in the path, as it's contained in the source and dest parameters
@router.post("/explorer/{data_source_id}/move")
def move(request_data: MoveRequest):  # noqa: E501
    use_case = MoveFileUseCase(get_repository=get_data_source)
    response = use_case.execute(request_data)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/remove")
def remove(data_source_id: str, remove_request: RemoveRequest):  # noqa: E501
    remove_request.data_source_id = data_source_id
    use_case = RemoveUseCase()
    response = use_case.execute(remove_request)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.post("/explorer/{data_source_id}/remove-by-path")
def remove_by_path(data_source_id: str, request: RemoveByPathRequest):  # noqa: E501
    request.data_source_id = data_source_id
    use_case = RemoveByPathUseCase()
    response = use_case.execute(request)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/explorer/{data_source_id}/rename")
def rename(data_source_id: str, request_data: RenameRequest):  # noqa: E501
    request_data.data_source_id = data_source_id
    use_case = RenameUseCase()
    response = use_case.execute(request_data)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
