from pathlib import Path

from pydantic.main import BaseModel

from domain_classes.user import User
from domain_classes.dto import DTO
from restful import response_object as res
from restful.use_case import UseCase
from storage.data_source_class import DataSource
from utils.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from utils.find_document_by_path import get_document_by_ref
from utils.logging import logger


class MoveRequest(BaseModel):
    source: str
    destination: str


class MoveFileUseCase(UseCase):
    def __init__(self, user: User, get_repository):
        self.user = user
        self.get_repository = get_repository

    def process_request(self, req: MoveRequest):
        source_data_source_id, source = req.source.split("/", 1)
        destination_data_source_uid, destination = req.destination.split("/", 1)
        source: Path = Path(req.source)
        destination: Path = Path(req.destination)

        # Check if the new destination package exists
        if different_parent := source.parent != destination.parent:
            new_parent_document = get_document_by_ref(
                f"{destination_data_source_uid}/{str(destination.parent)}", self.user
            )
            if not new_parent_document:
                raise EntityNotFoundException(req.destination)

        # Check if document already exists in destination
        if get_document_by_ref(req.destination, self.user):
            raise EntityAlreadyExistsException(req.destination)

        # Remove source document
        source_data_source = DataSource(uid=source_data_source_id, user=self.user)
        source_document_repository: DataSource = self.get_repository(source_data_source, user=self.user)
        source_document: DTO = get_document_by_ref(req.source, self.user)
        if not source_document:
            raise EntityNotFoundException(uid=f"{str(source)}")
        source_document_repository.delete(source_document.uid)
        logger.info(f"Removed document '{source_document.uid}' from data source '{source_data_source_id}'")

        # Add destination
        destination_data_source = DataSource(uid=destination_data_source_uid, user=self.user)
        destination_document_repository: DataSource = self.get_repository(destination_data_source)
        data = source_document.data
        data["name"] = destination.name
        destination_document = DTO(uid=source_document.uid, data=data)
        destination_document_repository.update(destination_document)
        logger.info(f"Added document '{destination_document.uid}' to data source '{destination_data_source_uid}")

        # Update parent(s)
        old_parent_document = get_document_by_ref(str(source.parent), self.user)
        reference = {"_id": source_document.uid, "name": destination.name, "type": source_document.type}
        # Remove old reference from parent
        old_parent_document.data["content"] = [
            ref for ref in old_parent_document.data["content"] if not ref["_id"] == source_document.uid
        ]
        # If the parent is not the same, insert ref to new parent.
        if different_parent:
            new_parent_document.data["content"].append(reference)
            destination_document_repository.update(new_parent_document)
        else:
            old_parent_document.data["content"].append(reference)
            source_document_repository.update(old_parent_document)

        return res.ResponseSuccess(destination_document)
