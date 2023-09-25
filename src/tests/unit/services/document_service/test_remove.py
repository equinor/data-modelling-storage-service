import unittest
from unittest import mock

from common.address import Address
from common.exceptions import ValidationException
from common.utils.data_structure.compare import get_and_print_diff
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.storage = {}
        self.repository = mock.Mock()
        self.repository.get = self.mock_get
        self.repository.update = self.mock_update
        self.repository.delete = self.mock_delete
        self.repository.delete_blob = self.mock_delete

        simos_blueprints = [
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Reference",
            "dmss://system/SIMOS/Blob",
        ]
        mock_blueprint_folder = "src/tests/unit/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "basic_blueprint": "basic_blueprint.blueprint.json",
            "uncontained_blueprint": "uncontained_blueprint.blueprint.json",
            "all_contained_cases_blueprint": "all_contained_cases_blueprint.blueprint.json",
            "blueprint_with_blob": "blueprint_with_blob.blueprint.json",
            "blueprint_with_optional_attr": "blueprint_with_optional_attr.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        self.mock_document_service = get_mock_document_service(
            repository_provider=lambda x, y: self.repository, blueprint_provider=self.mock_blueprint_provider
        )

    def mock_get(self, document_id: str):
        return self.storage[document_id]

    def mock_update(self, entity: dict, *args, **kwargs):
        self.storage[entity["_id"]] = entity

    def mock_delete(self, document_id: str):
        del self.storage[document_id]

    def test_remove_document(self):
        document_repository = mock.Mock()

        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "all_contained_cases_blueprint"}

        document_repository.get = lambda id: document_1.copy()

        self.mock_document_service.repository_provider = lambda id, user: document_repository
        self.mock_document_service.remove(Address("$1", "testing"))
        document_repository.delete.assert_called_with("1")

    def test_remove_document_wo_existing_blueprint(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "dmss://testing/this_blueprint_does_not_exist",
            }
        }
        self.mock_document_service.repository_provider = repository_provider = lambda x, y: self.repository
        self.assertRaises(FileNotFoundError, self.mock_document_service.remove, Address("$1", "testing"))

    def test_remove_document_with_model_and_storage_uncontained_children(self):
        doc_1 = {
            "uid": "1",
            "name": "Parent",
            "type": "uncontained_blueprint",
            "uncontained_in_every_way": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
        }
        doc_2 = {"uid": "2", "_id": "2", "name": "a_reference", "type": "basic_blueprint"}
        self.storage = {"1": doc_1, "2": doc_2}

        self.mock_document_service.remove(Address("$1", "testing"))
        assert get_and_print_diff(self.storage, {"2": doc_2}) == []

    def test_remove_required_child_dict_raises_validation_exception(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "all_contained_cases_blueprint",
                "nested": {
                    "address": "2",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.STORAGE.value,
                },
            },
            "2": {"name": "Nested", "description": "", "type": "basic_blueprint"},
        }

        self.assertRaises(
            ValidationException, self.mock_document_service.remove, Address("$1.nested", "testing", "dmss")
        )

    def test_remove_required_child_list_raises_validation_exception(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "all_contained_cases_blueprint",
                "references": [
                    {
                        "address": "2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    }
                ],
            },
            "2": {"name": "Nested", "description": "", "type": "basic_blueprint"},
        }

        self.assertRaises(ValidationException, self.mock_document_service.remove, Address("$1.references", "testing"))

    def test_remove_document_also_removes_storage_uncontained_children(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "all_contained_cases_blueprint",
                "nested": {
                    "name": "Nested",
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
                "type": "all_contained_cases_blueprint",
            },
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None

    def test_remove_document_also_removes_storage_uncontained_grand_children(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "all_contained_cases_blueprint",
                "nested": {
                    "name": "Nested",
                    "type": "all_contained_cases_blueprint",
                    "nested": {
                        "name": "Parent",
                        "type": "all_contained_cases_blueprint",
                        "references": [
                            {
                                "address": "2",
                                "type": SIMOS.REFERENCE.value,
                                "referenceType": REFERENCE_TYPES.STORAGE.value,
                            },
                            {
                                "address": "3",
                                "type": SIMOS.REFERENCE.value,
                                "referenceType": REFERENCE_TYPES.STORAGE.value,
                            },
                        ],
                    },
                },
            },
            "2": {
                "_id": "2",
                "name": "Parent",
                "type": "basic_blueprint",
            },
            "3": {
                "_id": "3",
                "name": "Parent",
                "type": "basic_blueprint",
            },
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None
        assert self.storage.get("3") is None

    def test_remove_required_reference_raises_validation_exception(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "all_contained_cases_blueprint",
                "reference": {
                    "address": "2",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
            "2": {"_id": "2", "name": "Reference", "type": "basic_blueprint"},
        }

        self.assertRaises(ValidationException, self.mock_document_service.remove, Address("$1.reference", "testing"))

    def test_remove_optional_attribute_is_removed_successfully(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "blueprint_with_optional_attr",
                "im_optional": {
                    "name": "old_entity",
                    "type": "basic_blueprint",
                    "description": "This is my old entity",
                },
            }
        }

        self.mock_document_service.remove(Address("$1.im_optional", "testing"))

        assert {
            "_id": "1",
            "name": "Parent",
            "type": "blueprint_with_optional_attr",
        } == self.storage["1"]

    def test_remove_blob(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "blueprint_with_blob",
                "blob": {"type": SIMOS.BLOB.value, "_blob_id": "blob_object"},
            },
            "blob_object": "someData",
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("blob_object") is None
