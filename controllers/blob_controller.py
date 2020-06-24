import json

from flask import Response, send_file

from api.core.use_case.get_blob_use_case import GetBlobUseCase
from controllers.status_codes import STATUS_CODES


def get_blob_by_id(data_source_id, blob_id):
    use_case = GetBlobUseCase()
    response = use_case.execute({"data_source": data_source_id, "blob_id": blob_id})
    if not response.type == "SUCCESS":
        return Response(json.dumps(response.value), mimetype="application/json", status=STATUS_CODES[response.type])
    return send_file(response.value, mimetype="application/octet-stream")
