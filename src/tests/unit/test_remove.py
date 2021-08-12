import unittest
from unittest import mock

from domain_classes.dto import DTO
from services.document_service import DocumentService

from tests.unit.mock_blueprint_provider import blueprint_provider
from utils.data_structure.compare import pretty_eq


class DocumentServiceTestCase(unittest.TestCase):
    def test_remove_document(self):
        document_repository = mock.Mock()

        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "blueprint_1"}

        document_repository.get = lambda id: DTO(data=document_1.copy())

        document_service = DocumentService(
            repository_provider=lambda id: document_repository, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1", parent_id=None)
        document_repository.delete.assert_called_with("1")

    def test_remove_document_with_model_and_storage_uncontained_children(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "uid": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {"_id": "2", "name": "a_reference", "type": "blueprint_2"},
            },
            "2": {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        def mock_delete(document_id: str):
            try:
                del doc_storage[document_id]
            except KeyError:
                pass

        repository.get = mock_get
        repository.update = mock_update
        repository.delete = mock_delete

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1", parent_id=None)
        expected = {"2": {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "blueprint_2"}}
        assert pretty_eq(expected, doc_storage) is None

    def test_remove_nested(self):
        document_repository = mock.Mock()

        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_1",
            "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return DTO(data=document_1.copy())
            return None

        document_repository.get = mock_get

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1.nested", parent_id="1")
        document_repository.update.assert_called_once()

    def test_remove_reference(self):
        document_repository = mock.Mock()

        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_1",
            "reference": {"_id": "2", "name": "Reference", "type": "blueprint_2"},
        }
        document_2 = {"_id": "2", "name": "Reference", "description": "", "type": "blueprint_2"}

        def mock_get(document_id: str):
            if document_id == "1":
                return DTO(data=document_1.copy())
            if document_id == "2":
                return DTO(data=document_2.copy())
            return None

        document_repository.get = mock_get

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="2", parent_id="1")
        document_repository.update.assert_called_once()
        document_repository.delete.assert_called_with("2")

    def test_remove_optional(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_optional_attr",
                "im_optional": {"name": "old_entity", "type": "blueprint_2", "description": "This is my old entity"},
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_optional_attr",
            "im_optional": {},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

        document_service.remove_document("testing", "1.im_optional", "1")

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None
