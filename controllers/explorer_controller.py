import json

from flask import request, Response

from api.core.repository.repository_factory import get_repository
from api.core.serializers.dto_json_serializer import DTOSerializer
from api.core.use_case.add_document_to_path_use_case import AddDocumentToPathRequestObject, AddDocumentToPathUseCase
from api.core.use_case.add_document_use_case import AddDocumentUseCase, AddDocumentRequestObject
from api.core.use_case.add_file_use_case import AddFileRequestObject, AddFileUseCase
from api.core.use_case.add_raw import AddRawRequestObject, AddRawUseCase
from api.core.use_case.add_root_package_use_case import AddRootPackageRequestObject, AddRootPackageUseCase
from api.core.use_case.move_file_use_case import MoveFileRequestObject, MoveFileUseCase
from api.core.use_case.remove_use_case import RemoveFileRequestObject, RemoveUseCase
from api.core.use_case.rename_file_use_case import RenameRequestObject, RenameUseCase
from controllers.status_codes import STATUS_CODES


def add_document(data_source_id, body):
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = AddDocumentUseCase()
    request_object = AddDocumentRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def add_to_parent(data_source_id, body):
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = AddFileUseCase()
    request_object = AddFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def add_to_path(data_source_id, body):
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = AddDocumentToPathUseCase()
    request_object = AddDocumentToPathRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def add_package(data_source_id, body):
    request_data = request.get_json()
    document_repository = get_repository(data_source_id)
    use_case = AddRootPackageUseCase(document_repository=document_repository, data_source_id=data_source_id)
    request_object = AddRootPackageRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)

    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def add_raw(data_source_id, body):
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = AddRawUseCase()
    request_object = AddRawRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def move(data_source_id, body):  # noqa: E501
    request_data = request.get_json()
    use_case = MoveFileUseCase(get_repository=get_repository)
    request_object = MoveFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def remove(data_source_id, body):  # noqa: E501
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = RemoveUseCase()
    request_object = RemoveFileRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )


def rename(data_source_id, body):  # noqa: E501
    request_data = request.get_json()
    request_data["data_source_id"] = data_source_id
    use_case = RenameUseCase()
    request_object = RenameRequestObject.from_dict(request_data)
    response = use_case.execute(request_object)
    return Response(
        json.dumps(response.value, cls=DTOSerializer), mimetype="application/json", status=STATUS_CODES[response.type]
    )
