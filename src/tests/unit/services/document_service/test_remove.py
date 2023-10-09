import unittest
from unittest import mock

import common.exceptions
from common.address import Address
from common.exceptions import ValidationException
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.storage = {}
        self.repository = mock.Mock()
        self.repository.get = lambda document_id: self.storage[document_id]
        self.repository.update = self.mock_update
        self.repository.delete = self.mock_delete
        self.repository.delete_blob = self.mock_delete

        simos_blueprints = [
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Reference",
            "dmss://system/SIMOS/Blob",
        ]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/people_and_cats"
        mock_blueprints_and_file_names = {
            "blob": "blob.blueprint.json",
            "Cat": "Cat.blueprint.json",
            "Person": "Person.blueprint.json",
            "PersonImage": "PersonImage.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )

        self.mock_document_service = get_mock_document_service(
            repository_provider=lambda x, y: self.repository, blueprint_provider=self.mock_blueprint_provider
        )

    def mock_update(self, entity: dict, *args, **kwargs):
        self.storage[entity["_id"]] = entity

    def mock_delete(self, document_id: str):
        del self.storage[document_id]

    def test_remove_document_removes_document_with_correct_id(self):
        document_repository = mock.Mock()

        document_1 = {"_id": "1", "name": "simple", "type": "dmss://system/SIMOS/NamedEntity"}

        document_repository.get = lambda id: document_1.copy()

        self.mock_document_service.repository_provider = lambda id, user: document_repository
        self.mock_document_service.remove(Address("$1", "testing"))
        document_repository.delete.assert_called_with("1")

    def test_remove_document_wo_existing_blueprint_raises_FileNotFoundError(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "no-exist",
                "type": "dmss://testing/this_blueprint_does_not_exist",
            }
        }
        self.mock_document_service.repository_provider = lambda x, y: self.repository
        self.assertRaises(FileNotFoundError, self.mock_document_service.remove, Address("$1", "testing"))

    def test_remove_document_with_model_and_storage_uncontained_children(self):
        doc_1 = {
            "uid": "1",
            "name": "Parent",
            "type": "Cat",
            "owner": {"_id": "2", "name": "a_reference", "type": "dmss://system/SIMOS/NamedEntity"},
        }
        doc_2 = {"uid": "2", "_id": "2", "name": "a_reference", "type": "dmss://system/SIMOS/NamedEntity"}
        self.storage = {"1": doc_1, "2": doc_2}

        self.mock_document_service.remove(Address("$1", "testing"))
        self.assertDictEqual(self.storage, {"2": doc_2})

    def test_remove_required_child_dict_raises_ValidationException(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "containedPersonInfo": {
                    "address": "2",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.STORAGE.value,
                },
            },
            "2": {"name": "Mary", "description": "", "type": "dmss://system/SIMOS/NamedEntity"},
        }

        self.assertRaises(
            ValidationException,
            self.mock_document_service.remove,
            Address("$1.containedPersonInfo", "testing", "dmss"),
        )

    def test_remove_required_primitive_attribute_raises_NotFoundException(self):
        self.storage = {"1": {"_id": "1", "name": "", "type": "dmss://system/SIMOS/NamedEntity", "description": ""}}

        self.assertRaises(
            common.exceptions.NotFoundException,
            self.mock_document_service.remove,
            Address("$1.description", "testing"),
        )

    def test_remove_required_child_list_raises_ValidationException(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "storageUncontainedListOfFriends": [
                    {
                        "address": "2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    }
                ],
            },
            "2": {"name": "", "description": "", "type": "dmss://system/SIMOS/NamedEntity"},
        }

        self.assertRaises(
            ValidationException,
            self.mock_document_service.remove,
            Address("$1.storageUncontainedListOfFriends", "testing"),
        )

    def test_remove_document_also_removes_storage_uncontained_children(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "bestFriend": {
                    "name": "Lisa",
                    "type": "Person",
                    "storageUncontainedBestFriend": {
                        "address": "2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    },
                },
            },
            "2": {
                "_id": "2",
                "name": "Mary",
                "type": "Person",
            },
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None

    def test_remove_document_also_removes_storage_uncontained_grand_children(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "",
                "type": "Person",
                "not_in_blueprint": {
                    "name": "John",
                    "type": "Person",
                    "not_in_blueprint": {
                        "name": "",
                        "type": "Person",
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
                "name": "Mary",
                "type": "dmss://system/SIMOS/NamedEntity",
            },
            "3": {
                "_id": "3",
                "name": "Lisa",
                "type": "dmss://system/SIMOS/NamedEntity",
            },
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("1") is None
        assert self.storage.get("2") is None
        assert self.storage.get("3") is None

    def test_remove_required_reference_raises_ValidationException(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "storageUncontainedBestFriend": {
                    "address": "2",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
            "2": {"_id": "2", "name": "Mary", "type": "dmss://system/SIMOS/NamedEntity"},
        }

        self.assertRaises(
            ValidationException,
            self.mock_document_service.remove,
            Address("$1.storageUncontainedBestFriend", "testing"),
        )

    def test_remove_optional_attribute_is_removed_successfully(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "type": "PersonImage",
                "optionalImageText": {
                    "name": "imageText",
                    "type": "dmss://system/SIMOS/NamedEntity",
                    "description": "This is my image text",
                },
            }
        }

        self.mock_document_service.remove(Address("$1.optionalImageText", "testing"))

        assert {
            "_id": "1",
            "name": "Parent",
            "type": "PersonImage",
        } == self.storage["1"]

    def test_remove_document_with_blob_removes_referenced_blob_object_as_well(self):
        self.storage = {
            "1": {
                "_id": "1",
                "name": "profilePic",
                "type": "PersonImage",
                "imageBlob": {"type": SIMOS.BLOB.value, "_blob_id": "blob_object"},
            },
            "blob_object": "someData",
        }

        self.mock_document_service.remove(Address("$1", "testing"))
        assert self.storage.get("blob_object") is None
