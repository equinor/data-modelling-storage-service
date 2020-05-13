from api.classes.dto import DTO

from api.core.storage.repository_exceptions import FileNotFoundException
from flask import Response

from api.core.storage.internal.data_source_factory import get_data_source

from api.core.service.document_service import DocumentService
import json


def get(data_source_id):
    document_service = DocumentService(repository_provider=get_data_source)
    root_packages = document_service.get_root_packages(data_source_id=data_source_id)
    return Response(
        json.dumps([package.to_dict() for package in root_packages]), mimetype="application/json", status=200
    )


def find_by_name(data_source_id, name):
    package: DTO = get_data_source(data_source_id).first(
        {"type": "system/SIMOS/Package", "isRoot": True, "name": name}
    )
    if not package:
        raise FileNotFoundException(data_source_id, name, is_root=True)
    return package.to_dict()["data"]
