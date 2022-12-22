import unittest

from common.tree_node_serializer import tree_node_from_dict, tree_node_to_dict
from common.utils.data_structure.compare import pretty_eq
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from tests.unit.mock_utils import flatten_dict, mock_storage_recipe_provider

all_contained_cases_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint1",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "reference"},
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "references",
            "dimensions": "*",
        },
    ],
}

basic_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint2",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        {"attributeType": "blueprint_3", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
    ],
}

blueprint_3 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint3",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        # This have to be optional, or else we will have an infinite loop caused by recursion
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "reference",
            "optional": True,
            "contained": False,
        },
    ],
}

blueprint_4 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint4",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        {
            "attributeType": "blueprint_4",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "a_list",
            "dimensions": "*",
        },
    ],
}

recursive_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "recursive",
    "description": "Second blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"attributeType": "recursive_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "im_me!"},
    ],
}


def get_blueprint(type: str):
    if type == "all_contained_cases_blueprint":
        return Blueprint(all_contained_cases_blueprint)
    if type == "basic_blueprint":
        return Blueprint(basic_blueprint)
    if type == "blueprint_3":
        return Blueprint(blueprint_3)
    if type == "blueprint_4":
        return Blueprint(blueprint_4)
    if type == "recursive_blueprint":
        return Blueprint(recursive_blueprint)
    return None


class TreenodeTestCase(unittest.TestCase):
    def test_is_root(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_data = {"name": "Nested", "description": "", "type": "basic_blueprint"}
        nested = Node(
            key="nested",
            uid="",
            entity=nested_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        assert root.is_root()
        assert not nested.is_root()

    def test_replace(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="",
            uid="1",
            entity=root_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_1_data = {"name": "Nested1", "description": "", "type": "basic_blueprint"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_2_data = {"name": "Nested2", "description": "", "type": "basic_blueprint"}
        nested_2 = Node(
            key="nested",
            uid="",
            entity=nested_2_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "description": "", "type": "basic_blueprint"},
        }

        assert actual_before == tree_node_to_dict(root)

        root.replace("1.nested", nested_2)

        actual_after_replaced = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested2", "description": "", "type": "basic_blueprint"},
        }

        assert actual_after_replaced == tree_node_to_dict(root)

    def test_delete_root_child(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_1_data = {"name": "Nested1", "description": "", "type": "basic_blueprint"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "description": "", "type": "basic_blueprint"},
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
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )

        nested_1_data = {"name": "Nested1", "description": "", "type": "basic_blueprint"}
        nested_1 = Node(
            key="nested",
            uid="",
            entity=nested_1_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
            recipe_provider=mock_storage_recipe_provider,
        )
        nested_2_data = {"name": "Nested2", "description": "", "type": "blueprint_3"}
        nested_2 = Node(
            key="nested2",
            uid="",
            entity=nested_2_data,
            blueprint_provider=get_blueprint,
            parent=nested_1,
            attribute=BlueprintAttribute(name="", attribute_type="blueprint_3"),
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
                "type": "basic_blueprint",
                "nested2": {"name": "Nested2", "description": "", "type": "blueprint_3"},
            },
        }

        assert actual_before == tree_node_to_dict(root)

        root.remove_by_path(["nested", "nested2"])

        actual_after_delete = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested1", "description": "", "type": "basic_blueprint"},
        }

        assert actual_after_delete == tree_node_to_dict(root)

    def test_delete_list_element_of_nested_child(self):
        document = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "blueprint_4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "blueprint_4",
                    "a_list": [
                        {"name": "Nested2-index-0", "description": "", "type": "blueprint_4", "a_list": []},
                        {"name": "Nested2-index-1", "description": "", "type": "blueprint_4", "a_list": []},
                    ],
                }
            ],
        }
        root = tree_node_from_dict(
            document, document.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )

        actual_before = {
            "_id": "1",
            "name": "root",
            "description": "",
            "type": "blueprint_4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "blueprint_4",
                    "a_list": [
                        {"name": "Nested2-index-0", "description": "", "type": "blueprint_4", "a_list": []},
                        {"name": "Nested2-index-1", "description": "", "type": "blueprint_4", "a_list": []},
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
            "type": "blueprint_4",
            "a_list": [
                {
                    "name": "Nested1",
                    "description": "",
                    "type": "blueprint_4",
                    "a_list": [{"name": "Nested2-index-0", "description": "", "type": "blueprint_4", "a_list": []}],
                }
            ],
        }

        assert actual_after_delete == tree_node_to_dict(root)

    def test_depth(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
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

        assert root.depth() == 0
        assert nested.depth() == 1

    def test_traverse(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested1",
                "description": "",
                "type": "basic_blueprint",
                "nested": {
                    "name": "Nested2",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
        }

        root = tree_node_from_dict(
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )
        result = [node.name for node in root.traverse()]
        # with error nodes
        # expected = ["Parent", "Nested1", "Nested2", "Reference", "nested", "reference", "references"]
        expected = ["Parent", "Nested1", "Nested2", "Reference", "nested", "reference", "nested", "references"]
        assert result == expected

    def test_traverse_reverse(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_data = {"name": "Nested1", "description": "", "type": "basic_blueprint"}
        nested = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_data,
            blueprint_provider=get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="basic_blueprint"),
        )

        nested_2_data = {"name": "Nested2", "description": "", "type": "blueprint_3"}
        nested_2 = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_2_data,
            blueprint_provider=get_blueprint,
            parent=nested,
            attribute=BlueprintAttribute(name="", attribute_type="blueprint_3"),
        )

        result = [node.name for node in nested_2.traverse_reverse()]
        expected = ["Nested2", "Nested1", "root"]
        assert result == expected

    def test_node_id(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
        root = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="",
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
        reference = Node(
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
            blueprint_provider=get_blueprint,
            parent=root,
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

        assert root.node_id == "1"
        assert nested.node_id == "1.nested"
        assert nested_2.node_id == "1.nested.nested"
        assert nested_2.node_id == "1.nested.nested"
        assert reference.node_id == "1.nested.nested.reference"
        assert list_node.node_id == "1.list"
        assert item_1.node_id == "1.list.0"

    def test_search(self):
        document_1 = {
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
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
                "reference": {},
                "references": [],
            },
        }

        root = tree_node_from_dict(
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )

        child_1 = root.search("1.nested.nested")

        assert child_1.node_id == "1.nested.nested"

        child_2 = root.search("1.nested.nested.reference")

        assert child_2.node_id == "1.nested.nested.reference"

    def test_get_by_keys(self):
        document_1 = {
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
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
        }

        root = tree_node_from_dict(
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )

        child_1 = root.get_by_path(["nested", "nested"])

        assert child_1.node_id == "1.nested.nested"

        child_2 = root.get_by_path(["nested", "nested", "reference"])

        assert child_2.uid == "2"

    def test_update(self):
        document_1 = {
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
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            "references": [],
        }

        root = tree_node_from_dict(
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )

        update_0 = {
            "name": "New-name",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "Some description",
                "type": "basic_blueprint",
                "nested": {
                    "name": "Nested",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            "references": [],
        }

        root.update(update_0)

        assert pretty_eq(update_0, tree_node_to_dict(root)) is None

        update_1 = {
            "name": "New-name",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "Some description",
                "type": "basic_blueprint",
                "nested": {
                    "name": "New-name",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            "references": [],
        }

        root.update(update_1)

        assert pretty_eq(update_1, tree_node_to_dict(root)) is None

        update_2 = {
            "name": "New-name",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {
                "name": "Nested",
                "description": "Some description",
                "type": "basic_blueprint",
                "nested": {
                    "name": "New-name",
                    "description": "",
                    "type": "blueprint_3",
                    "reference": {"_id": "2", "name": "New-name", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            "references": [],
        }

        root.update(update_2)

        assert pretty_eq(update_2, tree_node_to_dict(root)) is None

        expected = {
            "_id": "1",
            "name": "New-name",
            "type": "all_contained_cases_blueprint",
            "description": "",
            "nested": {
                "name": "Nested",
                "type": "basic_blueprint",
                "description": "Some description",
                "nested": {
                    "name": "New-name",
                    "type": "blueprint_3",
                    "description": "",
                    "reference": {"_id": "2", "name": "New-name", "type": "basic_blueprint", "description": ""},
                },
            },
            "reference": {"_id": "2", "name": "a_reference", "type": "basic_blueprint"},
            "references": [],
        }

        # reference and nested.nested.reference has uid and id generated since the tree now includes
        # nodes when attributes are missing, needed for having error nodes in the index.

        expected_flat = flatten_dict(expected)
        actual_flat = flatten_dict(tree_node_to_dict(root))
        # less than only works on flat dictionaries.
        assert expected_flat.items() <= actual_flat.items()

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
                        "_id": "5",
                        "name": "Reference",
                        "description": "",
                        "type": "basic_blueprint",
                        "_blueprint": basic_blueprint,
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
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
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
                    "reference": {"_id": "5", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "basic_blueprint"},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "basic_blueprint"},
            ],
        }

        assert pretty_eq(actual, tree_node_to_dict(root)) is None

    def test_recursive_from_dict(self):
        document_1 = {"_id": "1", "name": "Parent", "description": "", "type": "recursive_blueprint", "im_me!": {}}

        with self.assertRaises(RecursionError):
            tree_node_from_dict(
                document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
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
                        "_id": "5",
                        "name": "Reference",
                        "description": "",
                        "type": "basic_blueprint",
                        "_blueprint": basic_blueprint,
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
                    "reference": {"_id": "5", "name": "Reference", "description": "", "type": "basic_blueprint"},
                },
            },
            "reference": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
            "references": [
                {"_id": "3", "name": "Reference-1", "description": "", "type": "basic_blueprint"},
                {"_id": "4", "name": "Reference-2", "description": "", "type": "basic_blueprint"},
            ],
        }

        root = tree_node_from_dict(
            document_1, document_1.get("_id"), "", get_blueprint, recipe_provider=mock_storage_recipe_provider
        )

        assert pretty_eq(actual, tree_node_to_dict(root)) is None

    def test_to_dict(self):
        root_data = {"_id": 1, "name": "root", "description": "", "type": "all_contained_cases_blueprint"}
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
