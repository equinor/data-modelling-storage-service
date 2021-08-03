from fastapi import APIRouter
from starlette.responses import JSONResponse

from restful.status_codes import STATUS_CODES
from use_case.search_use_case import SearchRequest, SearchUseCase
from use_case.find_parent_package_use_case import FindParentPackageRequest, FindParentPackageUseCase
router = APIRouter()


@router.post("/search/{data_source_id}", operation_id="search", response_model=dict)
def search(data_source_id: str, request: dict):
    use_case = SearchUseCase()
    response = use_case.execute(SearchRequest(data_source_id=data_source_id, data=request))
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])

@router.get("/findParentPackage/{data_source_id}/{document_id}", operation_id="findParentPackage", response_model=dict)
def find_parent_package(data_source_id: str, document_id: str):
    use_case = FindParentPackageUseCase()
    package_id, is_root = use_case.execute(FindParentPackageRequest(data_source_id=data_source_id, document_id=document_id))
    return {"package_id": package_id, "is_root": is_root}


