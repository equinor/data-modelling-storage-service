from fastapi import APIRouter
from starlette.responses import JSONResponse

from api.core.storage.internal.data_source_repository import DataSourceRepository
from api.core.use_case.create_data_source_use_case import CreateDataSourceRequestObject, CreateDataSourceUseCase
from api.core.use_case.get_data_source_use_case import GetDataSourceUseCase, GetDataSourceUseCaseRequestObject
from api.core.use_case.get_data_sources_use_case import GetDataSourcesUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.get("/data-sources/{data_source_id}")
def get_data_source(data_source_id: str):
    data_source_repository = DataSourceRepository()
    use_case = GetDataSourceUseCase(data_source_repository)
    request_object = GetDataSourceUseCaseRequestObject.from_dict({"data_source_id": data_source_id})
    response = use_case.execute(request_object)
    return JSONResponse(
        {"name": response.value.name, "id": response.value.name}, status_code=STATUS_CODES[response.type]
    )


@router.post("/data-sources/{data_source_id}")
def save(data_source_id: str, request: dict):
    data_source_repository = DataSourceRepository()
    use_case = CreateDataSourceUseCase(data_source_repository=data_source_repository)
    request_object = CreateDataSourceRequestObject.from_dict({"dataSourceId": data_source_id, "formData": request})
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get("/data-sources")
def get_all():
    data_source_repository = DataSourceRepository()
    use_case = GetDataSourcesUseCase(data_source_repository)
    response = use_case.execute()
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
