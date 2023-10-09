import unittest

from common.tree.tree_node import ListNode, Node
from common.tree.tree_node_serializer import tree_node_to_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider


class TreeNodeToDictTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/NamedEntity"]
        mock_blueprint_folder = "src/tests/unit/common/tree/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "all_contained_cases_blueprint": "all_contained_cases_blueprint.blueprint.json",
            "Garden": "Garden.blueprint.json",
            "Bush": "Bush.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        ).get_blueprint

    def test_to_dict(self):
        root_data = {
            "_id": 1,
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "reference": {
                "name": "Reference-1",
                "description": "",
                "type": "Garden",
            },
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "Garden",
                "nested": {"name": "nested2", "type": "Bush"},
            },
            "references": [],
        }
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_data = {"name": "Nested", "description": "", "type": "Garden"}
        nested = Node(
            key="nested",
            uid="",
            entity=nested_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        nested_2_data = {"name": "Nested", "description": "", "type": "Bush"}
        nested_2 = Node(
            key="nested",
            uid="",
            entity=nested_2_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=nested,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
        )

        nested_2_reference_data = {"_id": "2", "name": "Reference", "description": "", "type": "Garden"}
        Node(
            key="reference",
            uid="2",
            entity=nested_2_reference_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=nested_2,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        list_data = {"name": "List", "type": "Bush"}
        list_node = ListNode(
            key="list",
            uid="",
            entity=list_data,
            parent=root,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
        )

        item_1_data = {"name": "Item1", "description": "", "type": "Garden"}
        item_1 = Node(
            key="0",
            uid="",
            entity=item_1_data,
            blueprint_provider=self.mock_blueprint_provider,
            parent=list_node,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        actual_root = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "Garden",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "Bush",
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "Garden"},
                },
            },
            "list": [{"name": "Item1", "description": "", "type": "Garden"}],
        }
        self.assertEqual(actual_root, tree_node_to_dict(root))

        actual_nested = {
            "name": "Nested",
            "description": "",
            "type": "Garden",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "Bush",
                "reference": {"_id": "2", "name": "Reference", "description": "", "type": "Garden"},
            },
        }
        item_1_actual = {"name": "Item1", "description": "", "type": "Garden"}

        self.assertEqual(actual_nested, tree_node_to_dict(nested))
        self.assertEqual(item_1_actual, tree_node_to_dict(item_1))


if __name__ == "__main__":
    unittest.main()
