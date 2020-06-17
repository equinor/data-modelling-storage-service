import json

from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source


class AddDocumentToPathRequestObject(req.ValidRequestObject):
    def __init__(self, data_source_id=None, directory=None, document=None, files=None):
        self.data_source_id = data_source_id
        self.directory = directory
        self.document = document
        self.files = files

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "document" not in adict:
            invalid_req.add_error("document", "is missing")

        try:
            document_json = json.loads(adict.get("document"))
        except Exception:
            invalid_req.add_error("failed to parse document to JSON")

        if "directory" not in adict:
            invalid_req.add_error("directory", "is missing")

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        # Leading "/" is optional. If it's there, remove it
        if adict.get("directory", "s")[0] == "/":
            dir_list = list(adict["directory"])
            dir_list.pop(0)
            adict["directory"] = "".join(dir_list)

        # Trailing "/" is optional. If it's there, remove it
        if adict.get("directory", "s")[-1] == "/":
            dir_list = list(adict["directory"])
            dir_list.pop(-1)
            adict["directory"] = "".join(dir_list)

        return cls(
            data_source_id=adict.get("data_source_id"),
            document=document_json,
            directory=adict.get("directory"),
            files=adict.get("files"),
        )


class AddDocumentToPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, request_object: AddDocumentToPathRequestObject):
        data_source_id = request_object.data_source_id
        directory: str = request_object.directory
        document: str = request_object.document
        files: dict = request_object.files

        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.add(
            data_source_id=data_source_id, directory=directory, document=document, files=files
        )
        return res.ResponseSuccess(document)
