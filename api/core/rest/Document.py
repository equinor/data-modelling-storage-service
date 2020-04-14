import json

from api.core.serializers.dto_json_serializer import DTOSerializer
from api.core.shared import response_object as res
from api.core.use_case.get_document_by_path_use_case import GetDocumentByPathUseCase, GetDocumentByPathRequestObject
from api.core.use_case.get_document_use_case import GetDocumentUseCase, GetDocumentRequestObject
from api.core.use_case.update_document_use_case import UpdateDocumentUseCase, UpdateDocumentRequestObject
from flask import Blueprint, Response, request
from api.utils.logging import logger

blueprint = Blueprint("document", __name__)

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.SYSTEM_ERROR: 500,
}


@blueprint.route("/api/v2/documents/<string:data_source_id>/<path:document_id>", methods=["GET"])
def get_by_id(data_source_id: str, document_id: str):
    logger.info(f"Getting document '{document_id}' from data source '{data_source_id}'")
    ui_recipe = request.args.get("ui_recipe")
    attribute = request.args.get("attribute")
    use_case = GetDocumentUseCase()
    request_object = GetDocumentRequestObject.from_dict(
        {"data_source_id": data_source_id, "document_id": document_id, "ui_recipe": ui_recipe, "attribute": attribute}
    )
    response = use_case.execute(request_object)
    return Response(json.dumps(response.value), mimetype="application/json", status=STATUS_CODES[response.type])


@blueprint.route("/api/v2/documents_by_path/<string:data_source_id>/<path:document_path>", methods=["GET"])
def get_by_path(data_source_id: str, document_path: str):
    logger.info(f"Getting document '{document_path}' from data source '{data_source_id}'")
    ui_recipe = request.args.get("ui_recipe")
    attribute = request.args.get("attribute")
    use_case = GetDocumentByPathUseCase()
    request_object = GetDocumentByPathRequestObject.from_dict(
        {"data_source_id": data_source_id, "path": document_path, "ui_recipe": ui_recipe, "attribute": attribute}
    )
    response = use_case.execute(request_object)
    return Response(json.dumps(response.value), mimetype="application/json", status=STATUS_CODES[response.type])


@blueprint.route("/api/v2/documents/<string:data_source_id>/<string:document_id>", methods=["PUT"])
def put(data_source_id: str, document_id: str):
    logger.info(f"Updating document '{document_id}' in data source '{data_source_id}'")
    data = request.get_json()
    attribute = request.args.get("attribute")
    request_object = UpdateDocumentRequestObject.from_dict(
        {"data_source_id": data_source_id, "data": data, "document_id": document_id, "attribute": attribute}
    )
    update_use_case = UpdateDocumentUseCase()
    response = update_use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )
