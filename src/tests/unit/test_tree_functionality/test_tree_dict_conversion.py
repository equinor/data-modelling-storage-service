import unittest

from common.tree_node_serializer import (
    tree_node_from_dict,
    tree_node_to_dict,
    tree_node_to_ref_dict,
)
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_utils import mock_storage_recipe_provider
from tests.unit.test_tree_functionality.blueprints_for_tree_tests import (
    all_contained_cases_blueprint,
    basic_blueprint,
    blueprint_3,
    get_blueprint,
)
from tests.unit.test_tree_functionality.get_node_for_tree_tests import (
    get_engine_package_node,
    get_form_example_node,
)


class TreeNodeDictConversion(unittest.TestCase):
    def test_from_dict(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "basic_blueprint",
                "_blueprint": basic_blueprint,
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "_blueprint": blueprint_3,
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
                "type": "basic_blueprint",
                "_blueprint": basic_blueprint,
            },
            "references": [
                {
                    "_id": "3",
                    "name": "Reference-1",
                    "description": "",
                    "type": "basic_blueprint",
                    "_blueprint": basic_blueprint,
                },
                {
                    "_id": "4",
                    "name": "Reference-2",
                    "description": "",
                    "type": "basic_blueprint",
                    "_blueprint": basic_blueprint,
                },
            ],
            "_blueprint": all_contained_cases_blueprint,
        }

        root = tree_node_from_dict(
            document_1, get_blueprint, uid=document_1.get("_id"), recipe_provider=mock_storage_recipe_provider
        )

        actual = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "basic_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint", "nested": {}},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "basic_blueprint", "nested": {}},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "basic_blueprint", "nested": {}},
            ],
        }

        assert get_and_print_diff(actual, tree_node_to_dict(root)) == []

    def test_recursive_from_dict(self):
        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "recursive_blueprint", "im_me!": {}}

        with self.assertRaises(RecursionError):
            tree_node_from_dict(
                document_1, get_blueprint, uid=document_1.get("_id"), recipe_provider=mock_storage_recipe_provider
            )

    def test_from_dict_using_dict_importer(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "basic_blueprint",
                "_blueprint": basic_blueprint,
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "_blueprint": blueprint_3,
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
                "type": "basic_blueprint",
                "_blueprint": basic_blueprint,
            },
            "references": [
                {
                    "_id": "3",
                    "name": "Reference-1",
                    "description": "",
                    "type": "basic_blueprint",
                    "_blueprint": basic_blueprint,
                },
                {
                    "_id": "4",
                    "name": "Reference-2",
                    "description": "",
                    "type": "basic_blueprint",
                    "_blueprint": basic_blueprint,
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
                "type": "basic_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {
                        "address": "$5",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint", "nested": {}},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "basic_blueprint", "nested": {}},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "basic_blueprint", "nested": {}},
            ],
        }

        root = tree_node_from_dict(
            document_1, get_blueprint, uid=document_1.get("_id"), recipe_provider=mock_storage_recipe_provider
        )

        assert get_and_print_diff(actual, tree_node_to_dict(root)) == []

    def test_to_dict(self):
        root_data = {
            "_id": 1,
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "reference": {
                "name": "Reference-1",
                "description": "",
                "type": "basic_blueprint",
            },
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "basic_blueprint",
                "nested": {"name": "nested2", "type": "blueprint_3"},
            },
            "references": [],
        }
        root = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_data = {"name": "Nested", "description": "", "type": "basic_blueprint"}
        nested = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
        )

        nested_2_data = {"name": "Nested", "description": "", "type": "blueprint_3"}
        nested_2 = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_2_data,
            blueprint_provider=get_blueprint,
            parent=nested,
            attribute=BlueprintAttribute(name="", attribute_type="blueprint_3"),
        )

        nested_2_reference_data = {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"}
        Node(
            recipe_provider=mock_storage_recipe_provider,
            key="reference",
            uid="2",
            entity=nested_2_reference_data,
            blueprint_provider=get_blueprint,
            parent=nested_2,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
        )

        list_data = {"name": "List", "type": "blueprint_3"}
        list_node = ListNode(
            recipe_provider=mock_storage_recipe_provider,
            key="list",
            uid="",
            entity=list_data,
            parent=root,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="blueprint_3"),
        )

        item_1_data = {"name": "Item1", "description": "", "type": "basic_blueprint"}
        item_1 = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="0",
            uid="",
            entity=item_1_data,
            blueprint_provider=get_blueprint,
            parent=list_node,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
        )

        actual_root = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "basic_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "list": [{"name": "Item1", "description": "", "type": "basic_blueprint"}],
        }

        self.assertEqual(actual_root, tree_node_to_dict(root))

        actual_nested = {
            "name": "Nested",
            "description": "",
            "type": "basic_blueprint",
            "nested": {
                "name": "Nested",
                "description": "",
                "type": "blueprint_3",
                "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
            },
        }

        self.assertEqual(actual_nested, tree_node_to_dict(nested))

        item_1_actual = {"name": "Item1", "description": "", "type": "basic_blueprint"}

        self.assertEqual(item_1_actual, tree_node_to_dict(item_1))

    def test_tree_node_to_ref_dict(self):
        engine_package_node = get_engine_package_node()
        engine_package_dict = tree_node_to_ref_dict(engine_package_node)
        assert engine_package_dict["content"][0] == {
            "address": "$123",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.STORAGE.value,
        }

    def test_tree_node_to_ref_dict_2(self):
        form_node = get_form_example_node()
        form_dict = tree_node_to_ref_dict(form_node)
        assert form_dict["inputEntity"] == {
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
            "address": "dmss://DemoDataSource/$product1",
        }
        # Check that optional attributes that don't exist on the node entity are not added by tree_node_to_ref_dict()
        assert "aOptionalNestedObject" not in form_node.entity and "aOptionalNestedObject" not in form_dict

    def test_from_dict_dimensions(self):
        doc = {
            "_id": "1",
            "type": "SignalContainer",
            "name": "signalContainer",
            "cases": [
                {"type": "Case", "name": "case1", "signal": {"type": "Signal", "values": [1, 2, 3, 4, 5, 6, 7]}}
            ],
        }

        root = tree_node_from_dict(
            doc, get_blueprint, uid=doc.get("_id"), recipe_provider=mock_storage_recipe_provider
        )
        case_list_attribute = root.children[0].attribute
        single_case_attribute = root.children[0].children[0].attribute
        assert case_list_attribute.dimensions.dimensions == ["*"]
        assert single_case_attribute.dimensions.dimensions == ""

    def test_from_dict_optional_values(self):
        doc = {
            "_id": "1",
            "type": "FormBlueprint",
            "name": "form",
            "aNestedObject": {"type": "NestedField", "bar": "..."},
            "inputEntity": {"type": "NestedField", "bar": "..."},
        }

        root = tree_node_from_dict(
            doc, get_blueprint, uid=doc.get("_id"), recipe_provider=mock_storage_recipe_provider
        )

        assert "aOptionalNestedObject" not in doc and "aOptionalNestedObject" not in tree_node_to_dict(root)
        assert "optionalNumberList" not in doc and "optionalNumberList" not in tree_node_to_dict(root)
        assert "optionalObjectList" not in doc and "optionalObjectList" not in tree_node_to_dict(root)

    def test_tree_node_to_ref_dict_for_references(self):
        reference_1 = {
            "address": "$22",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }
        reference_2 = {
            "address": "$33",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }
        uncontained_in_every_way = [reference_1, reference_2]
        document = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "uncontained_list_blueprint",
            "uncontained_in_every_way": [reference_1, reference_2],
        }

        parent_node: Node = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="",
            uid="1",
            entity=document,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="uncontained_list_blueprint"),
        )
        uncontained_in_every_way_node = ListNode(
            recipe_provider=mock_storage_recipe_provider,
            key="uncontained_in_every_way",
            uid="1.uncontained_in_every_way",
            entity=uncontained_in_every_way,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
        )
        reference_1_node = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="0",
            uid="1.uncontained_in_every_way.0",
            entity=reference_1,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="dmss://system/SIMOS/Reference"),
        )
        reference_2_node = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="1",
            uid="1.uncontained_in_every_way.1",
            entity=reference_2,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="dmss://system/SIMOS/Reference"),
        )
        uncontained_in_every_way_node.children.append(reference_1_node)
        uncontained_in_every_way_node.children.append(reference_2_node)
        parent_node.children.append(uncontained_in_every_way_node)
        parent_document = tree_node_to_ref_dict(parent_node)
        assert parent_document["uncontained_in_every_way"][0] == reference_1
        assert parent_document["uncontained_in_every_way"][1] == reference_2
