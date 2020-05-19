from api.core.repository.repository_factory import get_repository
from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.utility import get_document_by_ref


class GetDocumentByPathRequestObject(req.ValidRequestObject):
    def __init__(self, data_source_id, path, ui_recipe, attribute, depth):
        self.data_source_id = data_source_id
        self.path = path
        self.ui_recipe = ui_recipe
        self.attribute = attribute
        self.depth = depth

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if "path" not in adict:
            invalid_req.add_error("path", "is missing")

        try:
            depth = int(adict.get("depth", "999"))
            # Negative values will be treated as "disabling levels"
            if depth < 0:
                depth = 999
        except ValueError:
            depth = 999
            invalid_req.add_error("levels", "must be and integer")

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            data_source_id=adict.get("data_source_id"),
            path=adict.get("path"),
            ui_recipe=adict.get("ui_recipe"),
            attribute=adict.get("attribute"),
            depth=depth,
        )


class GetDocumentByPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_repository):
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider)

    def process_request(self, request_object: GetDocumentByPathRequestObject):
        data_source_id: str = request_object.data_source_id
        root_doc = get_document_by_ref(f"{data_source_id}/{request_object.path}")
        attribute: str = request_object.attribute

        document = self.document_service.get_by_uid(
            data_source_id=data_source_id, document_uid=root_doc.uid, depth=request_object.depth
        )

        if attribute:
            document = document.get_by_path(attribute.split("."))

        return res.ResponseSuccess({"document": document.to_dict()})
