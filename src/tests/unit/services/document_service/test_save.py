import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.address import Address
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import Node
from enums import REFERENCE_TYPES, SIMOS
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/NamedEntity", "dmss://system/SIMOS/Reference"]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/people_and_cats"
        mock_blueprints_and_file_names = {
            "Cat": "Cat.blueprint.json",
            "CoupleOfPeople": "CoupleOfPeople.blueprint.json",
            "Person": "Person.blueprint.json",
            "CatCage": "CatCage.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        self.mock_document_service = get_mock_document_service(blueprint_provider=self.mock_blueprint_provider)

    def test_save_update(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Johnny",
                "type": "Person",
                "containedPersonInfo": {"name": "", "type": "dmss://system/SIMOS/NamedEntity"},
                "storageUncontainedBestFriend": {
                    "_id": "2",
                    "name": "a_reference",
                    "type": "dmss://system/SIMOS/NamedEntity",
                },
                "storageUncontainedListOfFriends": [
                    {"_id": "3", "name": "ref1", "type": "dmss://system/SIMOS/NamedEntity"},
                    {"_id": "4", "name": "ref2", "type": "dmss://system/SIMOS/NamedEntity"},
                ],
            },
            "2": {"_id": "2", "name": "a_reference", "type": "dmss://system/SIMOS/NamedEntity"},
            "3": {"_id": "3", "name": "ref1", "type": "dmss://system/SIMOS/NamedEntity"},
            "4": {"_id": "4", "name": "ref2", "description": "TEST", "type": "dmss://system/SIMOS/NamedEntity"},
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda x, y: repository
        node: Node = self.mock_document_service.get_document(Address("$1", "testing"))
        contained_node: Node = node.get_by_path("storageUncontainedListOfFriends.1".split("."))
        contained_node.update(
            {"_id": "4", "name": "ref2", "description": "TEST_MODIFY", "type": "dmss://system/SIMOS/NamedEntity"}
        )
        for sub_node in node.traverse():
            if not sub_node.storage_contained and not sub_node.is_array():
                self.mock_document_service.save(node=sub_node, data_source_id="testing")

        assert doc_storage["4"] == {
            "_id": "4",
            "name": "ref2",
            "description": "TEST_MODIFY",
            "type": "dmss://system/SIMOS/NamedEntity",
        }

    def test_save_update_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "containedPersonInfo": {"name": "", "type": "dmss://system/SIMOS/NamedEntity"},
            }
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        self.mock_document_service.repository_provider = lambda x, y: repository

        contained_node: Node = self.mock_document_service.get_document(Address("$1.containedPersonInfo", "testing"))
        contained_node.update(
            {"name": "RENAMED", "description": "TEST_MODIFY", "type": "dmss://system/SIMOS/NamedEntity"}
        )
        self.mock_document_service.save(contained_node, "testing", initial=True)

        assert doc_storage["1"]["containedPersonInfo"]["description"] == "TEST_MODIFY"

    def test_save_append(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "containedPersonInfo": {"name": "JohnInfo", "type": "dmss://system/SIMOS/NamedEntity"},
                "storageUncontainedBestFriend": {"name": "Peter", "type": "dmss://system/SIMOS/NamedEntity"},
                "storageUncontainedListOfFriends": [],
            },
            "2": {"_id": "2", "name": "Mary", "type": "dmss://system/SIMOS/NamedEntity"},
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda x, y: repository

        node: Node = self.mock_document_service.get_document(Address("$1", "testing"))
        contained_node: Node = node.search("1.storageUncontainedListOfFriends")
        contained_node.children.append(
            Node(
                "0",
                uid="2",
                entity=doc_storage["2"],
                blueprint_provider=self.mock_document_service.get_blueprint,
                attribute=BlueprintAttribute(
                    name="storageUncontainedListOfFriends", attribute_type="dmss://system/SIMOS/NamedEntity"
                ),
            )
        )
        self.mock_document_service.save(node, "testing")

        assert doc_storage["1"]["storageUncontainedListOfFriends"] == [
            {
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.STORAGE.value,
                "address": "$2",
            }
        ]

    def test_save_delete(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "John",
                "type": "Person",
                "containedPersonInfo": {"name": "Nested", "type": "dmss://system/SIMOS/NamedEntity"},
                "storageUncontainedBestFriend": {
                    "_id": "2",
                    "name": "Mary",
                    "type": "dmss://system/SIMOS/NamedEntity",
                },
                "storageUncontainedListOfFriends": [
                    {
                        "address": "$2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    },
                    {
                        "address": "$3",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    },
                    {
                        "address": "$4",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.STORAGE.value,
                    },
                ],
            },
            "2": {
                "_id": "2",
                "name": "Gina",
                "description": "Index 1",
                "type": "dmss://system/SIMOS/NamedEntity",
            },
            "3": {
                "_id": "3",
                "name": "Lisa",
                "description": "Index 2",
                "type": "dmss://system/SIMOS/NamedEntity",
            },
            "4": {
                "_id": "4",
                "name": "Patricia",
                "description": "Index 3",
                "type": "dmss://system/SIMOS/NamedEntity",
            },
        }

        doc_1_after = {
            **doc_storage["1"],
            "storageUncontainedListOfFriends": [
                doc_storage["1"]["storageUncontainedListOfFriends"][0],
                doc_storage["1"]["storageUncontainedListOfFriends"][2],
            ],
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            repository.name = data_source_id
            if data_source_id == "testing":
                return repository

        self.mock_document_service.repository_provider = repository_provider

        node: Node = self.mock_document_service.get_document(Address("$1", "testing"))
        contained_node: Node = node.search("1.storageUncontainedListOfFriends")
        contained_node.remove_by_path(["1"])
        self.mock_document_service.save(node, "testing")

        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []
        assert doc_storage["3"] is not None

    def test_save_nested_uncontained(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "catCage",
                "description": "I'm the root document",
                "type": "CatCage",
                "cat": {
                    "type": "Cat",
                    "name": "Garfield",
                    "description": "I'm the first nested document, contained",
                    "owner": {
                        "type": SIMOS.REFERENCE.value,
                        "address": "$2",
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "2": {
                "_id": "2",
                "name": "John",
                "type": "dmss://system/SIMOS/NamedEntity",
                "description": "I am a cat owner, storage and model uncontained by my cat.",
            },
            "3": {
                "_id": "3",
                "name": "Lisa",
                "type": "dmss://system/SIMOS/NamedEntity",
                "description": "Lisa loves cats, and will take over as owner for John's cat, Garfield",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda id: doc_storage[id]
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda x, y: repository

        # Testing updating the reference
        node: Node = self.mock_document_service.get_document(Address("$1", "testing"))
        target_node = node.get_by_path(["cat", "owner"])
        target_node.update(doc_storage["3"])
        self.mock_document_service.save(node, "testing")
        assert doc_storage["1"]["cat"]["owner"] == {
            "address": "$3",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

    def test_save_no_overwrite_uncontained_document(self):
        repository = mock.Mock()

        cat_cage = {
            "_id": "1",
            "name": "catCage",
            "description": "I'm a cage for cats. ",
            "type": "CatCage",
            "cat": {
                "type": "Cat",
                "name": "Garfield",
                "description": "I'm a cat, meow.",
                "owner": {
                    "type": SIMOS.REFERENCE.value,
                    "address": "$2",
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
        }
        owner = {
            "_id": "2",
            "name": "owner",
            "type": "dmss://system/SIMOS/NamedEntity",
            "description": "I'm an owner for a cat. Model and storage uncontained from cat.",
        }

        doc_storage = {cat_cage["_id"]: cat_cage, owner["_id"]: owner}

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda id: deepcopy(doc_storage[id])
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda x, y: repository
        new_cage = cat_cage.copy()

        new_cat_description = "Changed"

        new_cage["cat"]["description"] = new_cat_description

        update_document_use_case(
            data=new_cage, address=Address("$1", "test"), document_service=self.mock_document_service
        )
        # Test that the "2" document has not been overwritten
        assert doc_storage["2"].get("description") == owner["description"]
        # Test that the "1" document has been updated
        assert doc_storage["1"]["cat"]["description"] == new_cat_description

    """
    This test tests that we can update a contained attribute, and all it's children (contained or not), without
    modifying the "root" document.
    """

    def test_save_update_children_of_contained_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "type": "CoupleOfPeople",
                "name": "GinaAndJohn",
                "a": {
                    "type": "Person",
                    "storageUncontainedBestFriend": {
                        "_id": "2",
                        "name": "Lisa",
                        "type": "dmss://system/SIMOS/NamedEntity",
                    },
                },
                "b": {},
            },
            "2": {"_id": "2", "name": "Lisa", "type": "dmss://system/SIMOS/NamedEntity"},
            "3": {"_id": "3", "description": " This is malformed, with missing type"},
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda x, y: repository
        new_data = {
            "name": "A-contained_attribute",
            "type": "Person",
            "description": "SOME DESCRIPTION",
            "storageUncontainedBestFriend": {
                "_id": "2",
                "name": "a_reference",
                "type": "dmss://system/SIMOS/NamedEntity",
                "description": "A NEW DESCRIPTION HERE",
            },
            "containedPersonInfo": {},
            "storageUncontainedListOfFriends": [],
        }
        update_document_use_case(
            data=new_data, address=Address("$1.a", "testing"), document_service=self.mock_document_service
        )

        assert doc_storage["1"]["a"]["description"] == "SOME DESCRIPTION"
        assert doc_storage["1"]["a"]["storageUncontainedBestFriend"]["description"] == "A NEW DESCRIPTION HERE"
        assert doc_storage["1"]["b"] == {}
