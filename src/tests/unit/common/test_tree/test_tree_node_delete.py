import unittest

from common.tree.tree_node import Node
from common.tree.tree_node_serializer import tree_node_from_dict, tree_node_to_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider


class TreeNodeDeleteTest(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = []
        mock_blueprint_folder = "src/tests/unit/common/test_tree/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "Blueprint4": "Blueprint4.blueprint.json",
            "Bush": "Bush.blueprint.json",
            "Garden": "Garden.blueprint.json",
            "all_contained_cases_blueprint": "all_contained_cases_blueprint.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        ).get_blueprint

    def test_delete_root_child(self):
        root_data = {"_id": 1, "name": "root", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_1_data = {"name": "Nested1", "type": "Garden"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "type": "Garden"},
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["nested"])

        actual_after_delete = {"_id": "1", "name": "root", "type": "all_contained_cases_blueprint"}

        assert actual_after_delete == tree_node_to_dict(root)

    def test_delete_nested_child(self):
        root_data = {"_id": 1, "name": "root", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_1_data = {"name": "Nested1", "type": "Garden"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )
        nested_2_data = {"name": "Nested2", "type": "Bush"}
        nested_2 = Node(
            key="nested2",
            uid="",
            entity=nested_2_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=nested_1,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested1",
                "type": "Garden",
                "nested2": {"name": "Nested2", "type": "Bush"},
            },
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["nested", "nested2"])

        actual_after_delete = {
            "_id": "1",
            "name": "root",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "type": "Garden"},
        }

        assert actual_after_delete == tree_node_to_dict(root)

    def test_delete_list_element_of_nested_child(self):
        document = {
            "_id": "1",
            "name": "root",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "type": "Blueprint4",
                    "a_list": [
                        {"name": "Nested2-index-0", "type": "Blueprint4", "a_list": []},
                        {"name": "Nested2-index-1", "type": "Blueprint4", "a_list": []},
                    ],
                }
            ],
        }
        root = tree_node_from_dict(
            document,
            self.mock_blueprint_provider,
            uid=document.get("_id"),
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "type": "Blueprint4",
                    "a_list": [
                        {"name": "Nested2-index-0", "type": "Blueprint4", "a_list": []},
                        {"name": "Nested2-index-1", "type": "Blueprint4", "a_list": []},
                    ],
                }
            ],
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["a_list", "0", "a_list", "1"])

        actual_after_delete = {
            "_id": "1",
            "name": "root",
            "type": "Blueprint4",
            "a_list": [
                {
                    "name": "Nested1",
                    "type": "Blueprint4",
                    "a_list": [{"name": "Nested2-index-0", "type": "Blueprint4", "a_list": []}],
                }
            ],
        }

        assert actual_after_delete == tree_node_to_dict(root)
