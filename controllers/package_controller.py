from api.classes.dto import DTO

from api.core.repository.repository_exceptions import FileNotFoundException
from flask import Response

from api.core.repository.repository_factory import get_repository

from api.core.service.document_service import DocumentService
import json


def get(data_source_id):
    document_service = DocumentService(repository_provider=get_repository)
    root_packages = document_service.get_root_packages(data_source_id=data_source_id)
    return Response(
        json.dumps([package.to_dict() for package in root_packages]), mimetype="application/json", status=200
    )


def find_by_name(data_source_id, name):
    package: DTO = get_repository(data_source_id).find(
        {"type": "system/DMT/Package", "isRoot": True, "name": name}, single=True
    )
    if not package:
        raise FileNotFoundException(data_source_id, name, is_root=True)
    return package.to_dict()["data"]
