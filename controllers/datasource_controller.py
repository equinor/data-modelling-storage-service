import json

from api.core.serializers.create_data_source_serializer import CreateDataSourceSerializer
from api.core.serializers.get_data_source_serializer import GetDataSourceSerializer


from api.core.use_case.create_data_source_use_case import CreateDataSourceUseCase, CreateDataSourceRequestObject
from api.core.use_case.get_data_source_use_case import GetDataSourceUseCase, GetDataSourceUseCaseRequestObject

from controllers.status_codes import STATUS_CODES

from api.core.serializers.get_data_sources_serializer import GetDataSourcesSerializer
from flask import request, Response

from api.core.use_case.get_data_sources_use_case import GetDataSourcesUseCase, GetDataSourcesUseCaseRequestObject

from api.core.repository.data_source_repository import DataSourceRepository


def get_data_source(data_source_id):
    data_source_repository = DataSourceRepository()
    use_case = GetDataSourceUseCase(data_source_repository)
    request_object = GetDataSourceUseCaseRequestObject.from_dict({"data_source_id": data_source_id})
    response = use_case.execute(request_object)
    return Response(json.dumps(response.value), mimetype="application/json", status=STATUS_CODES[response.type],)


def save(data_source_id):
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
