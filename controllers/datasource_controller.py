import json

from api.core.serializers.create_data_source_serializer import CreateDataSourceSerializer

from api.core.use_case.create_data_source_use_case import CreateDataSourceUseCase, CreateDataSourceRequestObject

from controllers.status_codes import STATUS_CODES

from api.core.serializers.get_data_sources_serializer import GetDataSourcesSerializer
from flask import request, Response

from api.core.use_case.get_data_sources_use_case import GetDataSourcesUseCase, GetDataSourcesUseCaseRequestObject

from api.core.repository.data_source_repository import DataSourceRepository


def save(data_source_id, body=None):
    data_source_repository = DataSourceRepository()
    use_case = CreateDataSourceUseCase(data_source_repository=data_source_repository)
    request_object = CreateDataSourceRequestObject.from_dict(
        {"dataSourceId": data_source_id, "formData": request.get_json()}
    )
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=CreateDataSourceSerializer),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )


def get_all():
    data_source_repository = DataSourceRepository()
    use_case = GetDataSourcesUseCase(data_source_repository)
    request_object = GetDataSourcesUseCaseRequestObject.from_dict(request.args)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=GetDataSourcesSerializer),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )
