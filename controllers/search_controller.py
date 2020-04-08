import json

from flask import request, Response

from api.core.serializers.dto_json_serializer import DTOSerializer
from api.core.use_case.search_use_case import SearchUseCase
from controllers.status_codes import STATUS_CODES


def search_entities(data_source_id: str):
    use_case = SearchUseCase()
    request_object = {"data_source_id": data_source_id, "data": request.get_json()}
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )
