import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.tree_node_serializer import tree_node_from_dict
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import Node
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_utils import (
    get_mock_document_service,
    mock_storage_recipe_provider,
)


class DocumentServiceTestCase(unittest.TestCase):
    def test_save_update(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
                "references": [
                    {"_id": "3", "name": "ref1", "type": "basic_blueprint"},
                    {"_id": "4", "name": "ref2", "type": "basic_blueprint"},
                ],
            },
            "2": {"_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"},
            "3": {"_id": "3", "name": "ref1", "description": "", "type": "basic_blueprint"},
            "4": {"_id": "4", "name": "ref2", "description": "TEST", "type": "basic_blueprint"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        node: Node = document_service.get_document("testing/$1")
        contained_node: Node = node.get_by_path("references.1".split("."))
        contained_node.update({"_id": "4", "name": "ref2", "description": "TEST_MODIFY", "type": "basic_blueprint"})
        document_service.save(node, "testing", update_uncontained=True)

        assert doc_storage["4"] == {
            "_id": "4",
            "name": "ref2",
            "description": "TEST_MODIFY",
            "type": "basic_blueprint",
        }

    def test_save_append(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {"name": "a_reference", "type": "basic_blueprint"},
                "references": [],
            },
            "2": {"_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        document_service = get_mock_document_service(lambda x, y: repository)

        node: Node = document_service.get_document("testing/$1")
        contained_node: Node = node.search("1.references")
        contained_node.children.append(
            Node(
                "0",
                uid="2",
                entity=doc_storage["2"],
                blueprint_provider=document_service.get_blueprint,
                attribute=BlueprintAttribute(name="references", attribute_type="basic_blueprint"),
            )
        )
        document_service.save(node, "testing")

        assert doc_storage["1"]["references"] == [
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
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
                "references": [
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
            "2": {"_id": "2", "name": "a_reference", "description": "Index 1", "type": "basic_blueprint"},
            "3": {"_id": "3", "name": "a_reference", "description": "Index 2", "type": "basic_blueprint"},
            "4": {"_id": "4", "name": "a_reference", "description": "Index 3", "type": "basic_blueprint"},
        }

        doc_1_after = {
            **doc_storage["1"],
            "references": [
                doc_storage["1"]["references"][0],
                doc_storage["1"]["references"][2],
            ],
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            repository.name = data_source_id
            if data_source_id == "testing":
                return repository

        document_service = get_mock_document_service(repository_provider)

        node: Node = document_service.get_document("testing/$1")
        contained_node: Node = node.search("1.references")
        contained_node.remove_by_path(["1"])
        document_service.save(node, "testing")

        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []
        assert doc_storage["3"] is not None

    def test_save_nested_uncontained(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Root",
                "description": "I'm the root document",
                "type": "blueprint_with_second_level_nested_uncontained_attribute",
                "i_have_a_uncontained_attribute": {
                    "type": "uncontained_blueprint",
                    "name": "first",
                    "description": "I'm the first nested document, contained",
                    "uncontained_in_every_way": {
                        "_id": "2",
                        "name": "im_a_uncontained_attribute",
                        "type": "basic_blueprint",
                        "description": "I'm the second nested document, uncontained",
                    },
                },
            },
            "3": {
                "_id": "3",
                "name": "ASelfContainedEntity",
                "type": "basic_blueprint",
                "description": "ASelfContainedEntity",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda id: doc_storage[id]
        repository.update = mock_update

        document_service = get_mock_document_service(lambda x, y: repository)

        node: Node = tree_node_from_dict(
            doc_storage["1"], document_service.get_blueprint, uid="1", recipe_provider=mock_storage_recipe_provider
        )
        document_service.save(node, "testing", update_uncontained=True)

        assert doc_storage["2"]["description"] == "I'm the second nested document, uncontained"
        assert (
            doc_storage["1"]["i_have_a_uncontained_attribute"]["uncontained_in_every_way"].get("description") == None
        )

        # Testing updating the reference
        node: Node = document_service.get_document("testing/$1")
        target_node = node.get_by_path(["i_have_a_uncontained_attribute", "uncontained_in_every_way"])
        target_node.update(doc_storage["3"])
        document_service.save(node, "testing")
        assert doc_storage["1"]["i_have_a_uncontained_attribute"]["uncontained_in_every_way"]["address"] == "$3"

    def test_save_no_overwrite_uncontained_document(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Root",
                "description": "I'm the root document",
                "type": "blueprint_with_second_level_nested_uncontained_attribute",
                "i_have_a_uncontained_attribute": {
                    "type": "uncontained_blueprint",
                    "name": "first",
                    "description": "I'm the first nested document, contained",
                    "uncontained_in_every_way": {
                        "type": SIMOS.REFERENCE.value,
                        "address": "$2",
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "2": {
                "_id": "2",
                "name": "im_a_uncontained_attribute",
                "type": "basic_blueprint",
                "description": "I'm the second nested document, uncontained",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda id: deepcopy(doc_storage[id])
        repository.update = mock_update

        document_service = get_mock_document_service(lambda x, y: repository)

        document_service.update_document(
            "test",
            "$1",
            data={
                "_id": "1",
                "name": "Root",
                "description": "I'm the root document",
                "type": "blueprint_with_second_level_nested_uncontained_attribute",
                "i_have_a_uncontained_attribute": {
                    "type": "uncontained_blueprint",
                    "name": "first",
                    "description": "This has changed!",
                    "uncontained_in_every_way": {
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                        "address": "$2",
                    },
                },
            },
            update_uncontained=False,
        )
        # Test that the "2" document has not been overwritten
        assert doc_storage["2"].get("description") == "I'm the second nested document, uncontained"
        assert doc_storage["1"]["i_have_a_uncontained_attribute"]["description"] == "This has changed!"

    """
    This test tests that we can update a contained attribute, and all it's children (contained or not), without
    modifying the "root" document.     
    """

    def test_save_update_children_of_contained_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "type": "two_contained_deep_attributes",
                "name": "Root",
                "a": {
                    "type": "all_contained_cases_blueprint",
                    "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
                },
                "b": {},
            },
            "2": {"_id": "2", "name": "a_reference", "description": "", "type": "basic_blueprint"},
            "3": {"_id": "3", "description": " This is malformed, with missing type"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)
        new_data = {
            "name": "A-contained_attribute",
            "type": "all_contained_cases_blueprint",
            "description": "SOME DESCRIPTION",
            "reference": {
                "_id": "2",
                "name": "a_reference",
                "type": "basic_blueprint",
                "description": "A NEW DESCRIPTION HERE",
            },
            "nested": {},
            "references": [],
        }
        document_service.update_document("testing", "$1", new_data, attribute="a", update_uncontained=True)

        assert doc_storage["1"]["a"]["description"] == "SOME DESCRIPTION"
        assert doc_storage["1"]["a"]["reference"]["description"] == "A NEW DESCRIPTION HERE"
        assert doc_storage["1"]["b"] == {}
