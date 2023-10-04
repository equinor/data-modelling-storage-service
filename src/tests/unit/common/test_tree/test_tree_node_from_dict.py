import json
import unittest

from common.tree.tree_node_serializer import tree_node_from_dict, tree_node_to_dict
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider

FILE_PATH = "src/tests/unit/common/test_tree/mock_data/mock_blueprints/"

with open(FILE_PATH + "Garden.blueprint.json") as f:
    Garden = json.load(f)

with open(FILE_PATH + "all_contained_cases_blueprint.blueprint.json") as f:
    all_contained_cases_blueprint = json.load(f)

with open(FILE_PATH + "Bush.blueprint.json") as f:
    Bush = json.load(f)


class TreeNodeFromDictTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/Reference"]
        mock_blueprint_folder = "src/tests/unit/common/test_tree/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "SignalContainer": "SignalContainer.blueprint.json",
            "all_contained_cases_blueprint": "all_contained_cases_blueprint.blueprint.json",
            "FormBlueprint": "FormBlueprint.blueprint.json",
            "Recursive": "Recursive.blueprint.json",
            "Garden": "Garden.blueprint.json",
            "Bush": "Bush.blueprint.json",
            "Signal": "Signal.blueprint.json",
            "NestedField": "NestedField.blueprint.json",
            "Case": "Case.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        ).get_blueprint

    def test_from_dict(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "Garden",
                "_blueprint": Garden,
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "Bush",
                    "_blueprint": Bush,
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {
                "_id": "2",
                "name": "Reference",
                "description": "",
                "type": "Garden",
                "_blueprint": Garden,
            },
            "references": [
                {
                    "_id": "3",
                    "name": "Reference-1",
                    "description": "",
                    "type": "Garden",
                    "_blueprint": Garden,
                },
                {
                    "_id": "4",
                    "name": "Reference-2",
                    "description": "",
                    "type": "Garden",
                    "_blueprint": Garden,
                },
            ],
            "_blueprint": all_contained_cases_blueprint,
        }

        root = tree_node_from_dict(
            document_1,
            self.mock_blueprint_provider,
            uid=document_1.get("_id"),
        )

        actual = {
            "_id": "1",
            "name": "Parent",
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
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "Garden", "nested": {}},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "Garden", "nested": {}},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "Garden", "nested": {}},
            ],
        }

        self.assertDictEqual(actual, tree_node_to_dict(root))

    def test_from_dict_using_dict_importer(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "Garden",
                "_blueprint": Garden,
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "Bush",
                    "_blueprint": Bush,
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {
                "_id": "2",
                "name": "Reference",
                "description": "",
                "type": "Garden",
                "_blueprint": Garden,
            },
            "references": [
                {
                    "_id": "3",
                    "name": "Reference-1",
                    "description": "",
                    "type": "Garden",
                    "_blueprint": Garden,
                },
                {
                    "_id": "4",
                    "name": "Reference-2",
                    "description": "",
                    "type": "Garden",
                    "_blueprint": Garden,
                },
            ],
            "_blueprint": all_contained_cases_blueprint,
        }

        actual = {
            "_id": "1",
            "name": "Parent",
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
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "Garden", "nested": {}},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "Garden", "nested": {}},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "Garden", "nested": {}},
            ],
        }

        root = tree_node_from_dict(
            document_1,
            self.mock_blueprint_provider,
            uid=document_1.get("_id"),
        )

        self.assertDictEqual(actual, tree_node_to_dict(root))

    def test_from_dict_optional_values(self):
        doc = {
            "_id": "1",
            "type": "FormBlueprint",
            "name": "form",
            "aNestedObject": {"type": "NestedField", "bar": "..."},
            "inputEntity": {"type": "NestedField", "bar": "..."},
        }

        root = tree_node_from_dict(doc, self.mock_blueprint_provider, uid=doc.get("_id"))

        assert "aOptionalNestedObject" not in doc and "aOptionalNestedObject" not in tree_node_to_dict(root)
        assert "optionalNumberList" not in doc and "optionalNumberList" not in tree_node_to_dict(root)
        assert "optionalObjectList" not in doc and "optionalObjectList" not in tree_node_to_dict(root)

    def test_recursive_from_dict(self):
        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "Recursive", "im_me!": {}}

        with self.assertRaises(RecursionError):
            tree_node_from_dict(
                document_1,
                self.mock_blueprint_provider,
                uid=document_1.get("_id"),
            )

    def test_from_dict_dimensions(self):
        doc = {
            "_id": "1",
            "type": "SignalContainer",
            "name": "signalContainer",
            "cases": [
                {"type": "Case", "name": "case1", "signal": {"type": "Signal", "values": [1, 2, 3, 4, 5, 6, 7]}}
            ],
        }

        root = tree_node_from_dict(doc, self.mock_blueprint_provider, uid=doc.get("_id"))
        case_list_attribute = root.children[0].attribute
        single_case_attribute = root.children[0].children[0].attribute
        assert case_list_attribute.dimensions.dimensions == ["*"]
        assert single_case_attribute.dimensions.dimensions == ""


if __name__ == "__main__":
    unittest.main()
