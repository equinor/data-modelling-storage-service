import unittest
from unittest import mock

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
                "type": "blueprint_1",
                "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
                "reference": {"_id": "2", "name": "a_reference", "type": "blueprint_2"},
                "references": [
                    {"_id": "3", "name": "ref1", "type": "blueprint_2"},
                    {"_id": "4", "name": "ref2", "type": "blueprint_2"},
                ],
            },
            "2": {"_id": "2", "name": "a_reference", "description": "", "type": "blueprint_2"},
            "3": {"_id": "3", "name": "ref1", "description": "", "type": "blueprint_2"},
            "4": {"_id": "4", "name": "ref2", "description": "TEST", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
        )

        node: Node = document_service.get_by_uid("testing", "1")
        contained_node: Node = node.get_by_path("references.1".split("."))
        contained_node.update({"_id": "4", "name": "ref2", "description": "TEST_MODIFY", "type": "blueprint_2"})
        document_service.save(node, "testing")

        assert doc_storage["4"] == {"_id": "4", "name": "ref2", "description": "TEST_MODIFY", "type": "blueprint_2"}

    def test_save_append(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "Parent", "description": "", "type": "blueprint_1", "references": []},
            "2": {"_id": "2", "name": "a_reference", "description": "", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
        )

        node: Node = document_service.get_by_uid("testing", "1")
        contained_node: Node = node.search("1.references")
        contained_node.children.append(
            Node(
                "0",
                uid="2",
                entity=doc_storage["2"],
                blueprint_provider=document_service.get_blueprint,
                attribute=BlueprintAttribute("references", "blueprint_2"),
            )
        )
        document_service.save(node, "testing")

        assert doc_storage["1"]["references"] == [{"name": "a_reference", "type": "blueprint_2", "_id": "2"}]

    def test_save_delete(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "references": [
                    {"_id": "2", "name": "a_reference", "type": "blueprint_2"},
                    {"_id": "3", "name": "a_reference", "type": "blueprint_2"},
                    {"_id": "4", "name": "a_reference", "type": "blueprint_2"},
                ],
            },
            "2": {"_id": "2", "name": "a_reference", "description": "Index 1", "type": "blueprint_2"},
            "3": {"_id": "3", "name": "a_reference", "description": "Index 2", "type": "blueprint_2"},
            "4": {"_id": "4", "name": "a_reference", "description": "Index 3", "type": "blueprint_2"},
        }

        doc_1_after = {
            "name": "Parent",
            "_id": "1",
            "description": "",
            "type": "blueprint_1",
            "nested": {},
            "reference": {},
            "references": [
                {"_id": "2", "name": "a_reference", "type": "blueprint_2"},
                {"_id": "4", "name": "a_reference", "type": "blueprint_2"},
            ],
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

        node: Node = document_service.get_by_uid("testing", "1")
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
                        "type": "blueprint_2",
                        "description": "I'm the second nested document, uncontained",
                    },
                },
            }
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
        )

        node: Node = Node.from_dict(doc_storage["1"], "1", document_service.get_blueprint)
        document_service.save(node, "testing")

        assert doc_storage["2"]["description"] == "I'm the second nested document, uncontained"
