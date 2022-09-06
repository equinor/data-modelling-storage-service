import unittest
from unittest import mock

from authentication.models import User
from common.utils.data_structure.compare import pretty_eq
from enums import SIMOS
from services.document_service import DocumentService
from tests.unit.mock_blueprint_provider import blueprint_provider


class DocumentServiceTestCase(unittest.TestCase):
    def test_remove_document(self):
        document_repository = mock.Mock()

        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "all_contained_cases_blueprint"}

        document_repository.get = lambda id: document_1.copy()

        document_service = DocumentService(
            repository_provider=lambda id, user: document_repository, blueprint_provider=blueprint_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1")
        document_repository.delete.assert_called_with("1")

    def test_remove_document_wo_existing_blueprint(self):
        repository = mock.Mock()
        doc_storage = {"1": {"_id": "1", "name": "Parent", "description": "", "type": "all_contained_cases_blueprint"}}

        class NoBlueprints:
            def get_blueprint(self, type):
                raise FileNotFoundError

        repository.get = lambda doc_id: doc_storage[doc_id]
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            blueprint_provider=NoBlueprints(), repository_provider=lambda x, y: repository
        )
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
                "uncontained_in_every_way": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            },
            "2": {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        def mock_delete(document_id: str):
            try:
                del doc_storage[document_id]
            except KeyError:
                pass

        repository.get = mock_get
        repository.update = mock_update
        repository.delete = mock_delete

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.remove_document(data_source_id="testing", document_id="1")
        expected = {"2": {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"}}
        assert pretty_eq(expected, doc_storage) is None

    def test_remove_nested(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            }
        }

        repository.get = lambda doc_id: doc_storage[doc_id]
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x, y: repository, blueprint_provider=blueprint_provider
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
                "type": "all_contained_cases_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "all_contained_cases_blueprint",
                    "nested": {
                        "_id": "2",
                        "name": "Parent",
                        "contained": True,
                        "type": "all_contained_cases_blueprint",
                    },
                },
            },
            "2": {
                "_id": "2",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
            },
        }

        repository.get = lambda doc_id: doc_storage[doc_id]
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x, y: repository, blueprint_provider=blueprint_provider
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
                "type": "all_contained_cases_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "all_contained_cases_blueprint",
                    "nested": [
                        {
                            "name": "Parent",
                            "type": "all_contained_cases_blueprint",
                            "nested": [
                                {
                                    "_id": "2",
                                    "name": "Parent",
                                    "contained": True,
                                    "type": "all_contained_cases_blueprint",
                                }
                            ],
                        },
                        {
                            "name": "Parent",
                            "type": "all_contained_cases_blueprint",
                            "nested": [
                                {
                                    "_id": "3",
                                    "name": "Parent",
                                    "contained": True,
                                    "type": "all_contained_cases_blueprint",
                                }
                            ],
                        },
                    ],
                },
            },
            "2": {
                "_id": "2",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
            },
            "3": {
                "_id": "3",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
            },
        }

        repository.get = lambda doc_id: doc_storage[doc_id]
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            repository_provider=lambda x, y: repository, blueprint_provider=blueprint_provider
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
                "type": "all_contained_cases_blueprint",
                "reference": {"_id": "2", "name": "Reference", "type": "basic_blueprint", "contained": False},
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
        }
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        repository.get = lambda uid: doc_storage[uid]

        def repository_provider(data_source_id, user: User):
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
            "type": "all_contained_cases_blueprint",
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
                "im_optional": {
                    "name": "old_entity",
                    "type": "basic_blueprint",
                    "description": "This is my old entity",
                },
            }
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def repository_provider(data_source_id, user: User):
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

    def test_remove_blob(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_blob",
                "blob": {"type": SIMOS.BLOB.value, "_blob_id": "blob_object"},
            },
            "blob_object": "someData",
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.delete = lambda doc_id: doc_storage.pop(doc_id)
        repository.delete_blob = lambda doc_id: doc_storage.pop(doc_id)
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.remove_document("testing", "1")
        assert doc_storage.get("blob_object") is None
