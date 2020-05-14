from api.classes.dto import DTO
from api.core.enums import DMT
from api.core.storage.data_source import DataSource
from api.core.storage.repository_exceptions import DuplicateFileNameException, FileNotFoundException
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.utils.logging import logger
from controllers.package_controller import find_by_name


class AddRootPackageRequestObject(req.ValidRequestObject):
    def __init__(self, name=None):
        self.name = name

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "name" not in adict or len(adict["name"]) == 0:
            invalid_req.add_error("name", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(name=adict.get("name"))


class AddRootPackageUseCase(uc.UseCase):
    def __init__(self, document_repository: DataSource, data_source_id):
        self.document_repository = document_repository
        self.data_source_id = data_source_id

    def process_request(self, request_object):
        name: str = request_object.name
        try:
            find_by_name(self.data_source_id, name)
        except FileNotFoundException:
            document: DTO = DTO(data={"name": name, "type": DMT.PACKAGE.value, "isRoot": True, "content": []})
            self.document_repository.add(document)
            logger.info(f"Added root package '{document.uid}'")

            return res.ResponseSuccess(document)
        else:
            raise DuplicateFileNameException(self.data_source_id, name)
