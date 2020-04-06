from flask import Response

from api.core.repository.repository_factory import get_repository

from api.core.service.document_service import DocumentService
import json


def get(data_source_id):
    document_service = DocumentService(repository_provider=get_repository)
    root_packages = document_service.get_root_packages(data_source_id=data_source_id)
    print(root_packages)
    return Response(json.dumps([package.to_dict() for package in root_packages]), mimetype="application/json", status=200)
