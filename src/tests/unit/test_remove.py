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
        document_service.remove_document(data_source_id="testing", document_id="1")
        document_repository.delete.assert_called_with("1")

    def test_remove_document_wo_existing_blueprint(self):
        repository = mock.Mock()
        doc_storage = {"1": {"_id": "1", "name": "Parent", "description": "", "type": "blueprint_1"}}

        class NoBlueprints:
            def get_blueprint(self, type):
                raise FileNotFoundError

        repository.get = lambda doc_id: DTO(doc_storage[doc_id])
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(blueprint_provider=NoBlueprints(), repository_provider=lambda x: repository)
        document_service.remove_document(data_source_id="testing", document_id="1")
        assert doc_storage == {}

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
        document_service.remove_document(data_source_id="testing", document_id="1")
        expected = {"2": {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "blueprint_2"}}
        assert pretty_eq(expected, doc_storage) is None

    def test_remove_nested(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
            }
        }

        repository.get = lambda doc_id: DTO(doc_storage[doc_id])
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x: repository, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1.nested")
        assert doc_storage["1"].get("nested") is None

    def test_remove_second_level_nested(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_1",
                    "nested": {"_id": "2", "name": "Parent", "contained": True, "type": "blueprint_1"},
                },
            },
            "2": {"_id": "2", "name": "Parent", "description": "", "type": "blueprint_1",},
        }

        repository.get = lambda doc_id: DTO(doc_storage[doc_id])
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x: repository, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1")
        assert doc_storage.get("1") is None
        assert doc_storage.get("2") is None

    def test_remove_third_level_nested_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_1",
                    "nested": [
                        {
                            "name": "Parent",
                            "type": "blueprint_1",
                            "nested": [{"_id": "2", "name": "Parent", "contained": True, "type": "blueprint_1"}],
                        },
                        {
                            "name": "Parent",
                            "type": "blueprint_1",
                            "nested": [{"_id": "3", "name": "Parent", "contained": True, "type": "blueprint_1"}],
                        },
                    ],
                },
            },
            "2": {"_id": "2", "name": "Parent", "description": "", "type": "blueprint_1",},
            "3": {"_id": "3", "name": "Parent", "description": "", "type": "blueprint_1",},
        }

        repository.get = lambda doc_id: DTO(doc_storage[doc_id])
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x: repository, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1")
        assert doc_storage.get("1") is None
        assert doc_storage.get("2") is None
        assert doc_storage.get("3") is None

    def test_remove_reference(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "reference": {"_id": "2", "name": "Reference", "type": "blueprint_2", "contained": False},
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "blueprint_2"},
        }
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        repository.get = lambda uid: DTO(doc_storage[uid])

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1.reference")
        assert doc_storage["1"] == {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_1",
        }
        assert doc_storage.get("2")

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

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.remove_document("testing", "1.im_optional")
        assert {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_optional_attr",
        } == doc_storage["1"]
