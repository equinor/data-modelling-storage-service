import unittest
from copy import deepcopy
from unittest import mock

from common.utils.data_structure.compare import get_and_print_diff
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_utils import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.storage = {}
        self.repository = mock.Mock()
        self.repository.get = self.mock_get
        self.repository.update = self.mock_update
        self.repository.delete = self.mock_delete
        self.repository.delete_blob = self.mock_delete
        self.document_service = get_mock_document_service(lambda x, y: self.repository)

    def mock_get(self, document_id: str):
        return deepcopy(self.storage[document_id])

    def mock_update(self, entity: dict, *args, **kwargs):
        self.storage[entity["_id"]] = entity

    def mock_delete(self, document_id: str):
        del self.storage[document_id]

    def test_remove_document(self):
        document_repository = mock.Mock()

        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "all_contained_cases_blueprint"}

        document_repository.get = lambda id: document_1.copy()

        document_service = get_mock_document_service(lambda id, user: document_repository)
        document_service.remove("/testing/$1")
        document_repository.delete.assert_called_with("1")

    def test_remove_document_wo_existing_blueprint(self):
        self.storage = {
            "1": {"_id": "1", "name": "Parent", "description": "", "type": "all_contained_cases_blueprint"}
        }

        class NoBlueprints:
            def get_blueprint(self, type):
                raise FileNotFoundError

        self.document_service = get_mock_document_service(
            blueprint_provider=NoBlueprints(),
            repository_provider=lambda x, y: self.repository,
        )
        self.document_service.remove("/testing/$1")
        assert self.storage == {}

    def test_remove_document_with_model_and_storage_uncontained_children(self):
        doc_1 = {
            "uid": "1",
            "name": "Parent",
            "description": "",
            "type": "uncontained_blueprint",
            "uncontained_in_every_way": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
        }
        doc_2 = {"uid": "2", "_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"}
        self.storage = {"1": doc_1, "2": doc_2}

        self.document_service.remove("/testing/$1")
        assert get_and_print_diff(self.storage, {"2": doc_2}) == []

    def test_remove_nested(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            }
        }

        self.document_service.remove("/testing/$1.nested")
        assert self.storage["1"].get("nested") is None

    def test_remove_second_level_nested(self):
        self.storage = {
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
                        "address": "2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
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

        self.document_service.remove("/testing/$1")
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None

    def test_remove_third_level_nested_list(self):
        self.storage = {
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
                                    "address": "2",
                                    "type": SIMOS.REFERENCE.value,
                                    "referenceType": REFERENCE_TYPES.STORAGE.value,
                                }
                            ],
                        },
                        {
                            "name": "Parent",
                            "type": "all_contained_cases_blueprint",
                            "nested": [
                                {
                                    "address": "3",
                                    "type": SIMOS.REFERENCE.value,
                                    "referenceType": REFERENCE_TYPES.STORAGE.value,
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

        self.document_service.remove("/testing/$1")
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None
        assert self.storage.get("3") is None

    def test_remove_reference(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "reference": {
                    "address": "2",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
        }

        self.document_service.remove("/testing/$1.reference")
        assert self.storage["1"] == {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
        }
        assert self.storage.get("2")

    def test_remove_optional(self):
        self.storage = {
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

        self.document_service.remove("/testing/$1.im_optional")
        assert {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_optional_attr",
        } == self.storage["1"]

    def test_remove_blob(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_blob",
                "blob": {"type": SIMOS.BLOB.value, "_blob_id": "blob_object"},
            },
            "blob_object": "someData",
        }

        self.document_service.remove("/testing/$1")
        assert self.storage.get("blob_object") is None
