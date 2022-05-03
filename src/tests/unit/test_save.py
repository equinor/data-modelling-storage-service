import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from tests.unit.mock_blueprint_provider import blueprint_provider, flatten_dict


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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        node: Node = document_service.get_node_by_uid("testing", "1")
        contained_node: Node = node.get_by_path("references.1".split("."))
        contained_node.update({"_id": "4", "name": "ref2", "description": "TEST_MODIFY", "type": "basic_blueprint"})
        document_service.save(node, "testing")

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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        node: Node = document_service.get_node_by_uid("testing", "1")
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
            {"name": "a_reference", "type": "basic_blueprint", "_id": "2", "contained": True}
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
                    {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
                    {"_id": "3", "name": "a_reference", "type": "basic_blueprint"},
                    {"_id": "4", "name": "a_reference", "type": "basic_blueprint"},
                ],
            },
            "2": {"_id": "2", "name": "a_reference", "description": "Index 1", "type": "basic_blueprint"},
            "3": {"_id": "3", "name": "a_reference", "description": "Index 2", "type": "basic_blueprint"},
            "4": {"_id": "4", "name": "a_reference", "description": "Index 3", "type": "basic_blueprint"},
        }

        doc_1_after = {
            "name": "Parent",
            "_id": "1",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {},
            "reference": {},
            "references": [
                {"_id": "2", "name": "a_reference", "type": "basic_blueprint", "contained": True},
                {"_id": "4", "name": "a_reference", "type": "basic_blueprint", "contained": True},
            ],
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

        node: Node = document_service.get_node_by_uid("testing", "1")
        contained_node: Node = node.search("1.references")
        contained_node.remove_by_path(["1"])
        document_service.save(node, "testing")

        assert flatten_dict(doc_1_after).items() <= flatten_dict(doc_storage["1"]).items()
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

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = lambda id: DTO(doc_storage[id])
        repository.update = mock_update

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        node: Node = Node.from_dict(doc_storage["1"], "1", document_service.get_blueprint)
        document_service.save(node, "testing", update_uncontained=True)

        assert doc_storage["2"]["description"] == "I'm the second nested document, uncontained"
        assert (
            doc_storage["1"]["i_have_a_uncontained_attribute"]["uncontained_in_every_way"].get("description") == None
        )

        # Testing updating the reference
        node: Node = document_service.get_node_by_uid("testing", "1")
        target_node = node.get_by_path(["i_have_a_uncontained_attribute", "uncontained_in_every_way"])
        target_node.update(doc_storage["3"])
        document_service.save(node, "testing")
        assert doc_storage["1"]["i_have_a_uncontained_attribute"]["uncontained_in_every_way"]["_id"] == "3"

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
                        "_id": "2",
                        "name": "im_a_uncontained_attribute",
                        "type": "basic_blueprint",
                        "contained": False,
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

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = lambda id: DTO(deepcopy(doc_storage[id]))
        repository.update = mock_update

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        document_service.update_document(
            "test",
            "1",
            {
                "_id": "1",
                "name": "Root",
                "description": "I'm the root document",
                "type": "blueprint_with_second_level_nested_uncontained_attribute",
                "i_have_a_uncontained_attribute": {
                    "type": "uncontained_blueprint",
                    "name": "first",
                    "description": "This has changed!",
                    "uncontained_in_every_way": {
                        "_id": "2",
                        "name": "im_a_uncontained_attribute",
                        "type": "basic_blueprint",
                        "contained": False,
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )
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
        document_service.update_document("testing", "1.a", new_data, update_uncontained=True)

        assert doc_storage["1"]["a"]["description"] == "SOME DESCRIPTION"
        assert doc_storage["1"]["a"]["reference"]["description"] == "A NEW DESCRIPTION HERE"
        assert doc_storage["1"]["b"] == {}
