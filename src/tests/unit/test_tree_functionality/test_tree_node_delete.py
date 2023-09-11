import unittest

from common.tree_node_serializer import tree_node_from_dict, tree_node_to_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import Node
from tests.unit.mock_data.mock_recipe_provider import mock_storage_recipe_provider
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_document_service_for_tree_tests import (
    mock_document_service,
)


class TreeNodeDeleteTest(unittest.TestCase):
    def test_delete_root_child(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=mock_document_service.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_1_data = {"name": "Nested1", "description": "", "type": "Garden"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=mock_document_service.get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
            recipe_provider=mock_storage_recipe_provider,
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "description": "", "type": "Garden"},
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["nested"])

        actual_after_delete = {"_id": "1", "name": "root", "description": "", "type": "all_contained_cases_blueprint"}

        assert actual_after_delete == tree_node_to_dict(root)

    def test_delete_nested_child(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=mock_document_service.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_1_data = {"name": "Nested1", "description": "", "type": "Garden"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=mock_document_service.get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
            recipe_provider=mock_storage_recipe_provider,
        )
        nested_2_data = {"name": "Nested2", "description": "", "type": "Bush"}
        nested_2 = Node(
            key="nested2",
            uid="",
            entity=nested_2_data,
            blueprint_provider=mock_document_service.get_blueprint,
            parent=nested_1,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
            recipe_provider=mock_storage_recipe_provider,
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested1",
                "description": "",
                "type": "Garden",
                "nested2": {"name": "Nested2", "description": "", "type": "Bush"},
            },
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["nested", "nested2"])

        actual_after_delete = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "description": "", "type": "Garden"},
        }

        assert actual_after_delete == tree_node_to_dict(root)

    def test_delete_list_element_of_nested_child(self):
        document = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "Blueprint4",
                    "a_list": [
                        {"name": "Nested2-index-0", "description": "", "type": "Blueprint4", "a_list": []},
                        {"name": "Nested2-index-1", "description": "", "type": "Blueprint4", "a_list": []},
                    ],
                }
            ],
        }
        root = tree_node_from_dict(
            document,
            mock_document_service.get_blueprint,
            uid=document.get("_id"),
            recipe_provider=mock_storage_recipe_provider,
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "Blueprint4",
                    "a_list": [
                        {"name": "Nested2-index-0", "description": "", "type": "Blueprint4", "a_list": []},
                        {"name": "Nested2-index-1", "description": "", "type": "Blueprint4", "a_list": []},
                    ],
                }
            ],
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["a_list", "0", "a_list", "1"])

        actual_after_delete = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "Blueprint4",
                    "a_list": [{"name": "Nested2-index-0", "description": "", "type": "Blueprint4", "a_list": []}],
                }
            ],
        }

        assert actual_after_delete == tree_node_to_dict(root)
