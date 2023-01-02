import unittest
from unittest import mock

from common.tree_node_serializer import tree_node_to_dict
from common.utils.data_structure.compare import pretty_eq
from tests.unit.mock_utils import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def test_get_complete_document(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            "reference": {"_id": "2", "name": "Reference", "type": "basic_blueprint"},
            "references": [
                {"_id": "3", "name": "Reference1", "type": "basic_blueprint"},
                {"_id": "4", "name": "Reference2", "type": "basic_blueprint"},
            ],
        }

        document_2 = {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"}
        document_3 = {"_id": "3", "name": "Reference1", "description": "", "type": "basic_blueprint"}
        document_4 = {"_id": "4", "name": "Reference2", "description": "", "type": "basic_blueprint"}

        def mock_get(document_id: str):
            if document_id == "1":
                return document_1.copy()
            if document_id == "2":
                return document_2.copy()
            if document_id == "3":
                return document_3.copy()
            if document_id == "4":
                return document_4.copy()
            return None

        document_repository = mock.Mock()
        document_repository.get = mock_get

        document_service = get_mock_document_service(lambda x, y: document_repository)
        root = tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

        assert isinstance(root, dict)

        actual = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            "reference": document_2,
            "references": [document_3, document_4],
        }

        assert pretty_eq(actual, root) is None

    def test_get_complete_nested_reference(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_second_level_reference",
            "contained_with_child_references": {
                "name": "First child",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {"_id": "2", "name": "Reference", "type": "basic_blueprint"},
                "references": [
                    {"_id": "3", "name": "Reference1", "type": "basic_blueprint"},
                    {"_id": "4", "name": "Reference2", "type": "basic_blueprint"},
                ],
            },
        }

        document_2 = {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"}
        document_3 = {"_id": "3", "name": "Reference1", "description": "", "type": "basic_blueprint"}
        document_4 = {"_id": "4", "name": "Reference2", "description": "", "type": "basic_blueprint"}

        def mock_get(document_id: str):
            if document_id == "1":
                return document_1.copy()
            if document_id == "2":
                return document_2.copy()
            if document_id == "3":
                return document_3.copy()
            if document_id == "4":
                return document_4.copy()
            return None

        document_repository = mock.Mock()
        document_repository.get = mock_get

        document_service = get_mock_document_service(lambda x, y: document_repository)
        root = tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

        assert isinstance(root, dict)

        actual = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_second_level_reference",
            "contained_with_child_references": {
                "name": "First child",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": document_2,
                "references": [document_3, document_4],
            },
        }

        assert pretty_eq(actual, root) is None
