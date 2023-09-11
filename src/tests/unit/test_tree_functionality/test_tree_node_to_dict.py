import unittest
from unittest import skip

from common.exceptions import BadRequestException
from common.tree_node_serializer import tree_node_to_dict, tree_node_to_ref_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_blueprint_provider_for_tree_tests import (
    BlueprintProvider,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_document_service_for_tree_tests import (
    mock_document_service,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_storage_recipe_provider import (
    mock_storage_recipe_provider,
)


class TreeNodeToDictTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.attribute = BlueprintAttribute(name="a", attribute_type="dmss://system/SIMOS/BlueprintAttribute")
        self.node = Node(key="1", attribute=self.attribute, blueprint_provider=mock_document_service.get_blueprint)

    def test_to_dict_on_node_with_no_entity_returns_empty_dict(self):
        node_dict = tree_node_to_dict(self.node)
        assert len(node_dict.items()) == 0

    def test_to_dict_when_node_entity_has_no_type_raises_BadRequestException(self):
        self.node.entity = {"name": "entity-without-type"}
        with self.assertRaises(BadRequestException):
            tree_node_to_dict(self.node)

    def test_to_dict_when_node_contains_a_simple_entity_returns_dict_with_the_entity(self):
        self.node.entity = {"type": "Flower"}

        node_dict = tree_node_to_dict(self.node)
        assert len(node_dict.items()) == 1
        assert node_dict["type"] == "Flower"

    @skip
    def test_to_dict_when_node_contains_entity_of_invalid_type_throws(self):
        raise NotImplementedError

    @skip
    def test_to_dict_when_node_is_array_returns_list_of_dicts(self):
        raise NotImplementedError

    @skip
    def test_to_dict_when_node_is_array_returns_list_of_dicts_with_correct_type_and_attributes(self):
        raise NotImplementedError

    @skip
    def test_to_dict_when_node_contains_no_blueprint_only_type_is_in_dict(self):
        raise NotImplementedError

    @skip
    def test_to_dict_when_node_contains_blueprint_all_attributes_are_in_dict(self):
        raise NotImplementedError

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
            recipe_provider=mock_storage_recipe_provider,
            key="root",
            uid="1",
            entity=root_data,
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="all_contained_cases_blueprint"),
        )

        nested_data = {"name": "Nested", "description": "", "type": "Garden"}
        nested = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_data,
            blueprint_provider=BlueprintProvider.get_blueprint,
            parent=root,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        nested_2_data = {"name": "Nested", "description": "", "type": "Bush"}
        nested_2 = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="nested",
            uid="",
            entity=nested_2_data,
            blueprint_provider=BlueprintProvider.get_blueprint,
            parent=nested,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
        )

        nested_2_reference_data = {"_id": "2", "name": "Reference", "description": "", "type": "Garden"}
        Node(
            recipe_provider=mock_storage_recipe_provider,
            key="reference",
            uid="2",
            entity=nested_2_reference_data,
            blueprint_provider=BlueprintProvider.get_blueprint,
            parent=nested_2,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )

        list_data = {"name": "List", "type": "Bush"}
        list_node = ListNode(
            recipe_provider=mock_storage_recipe_provider,
            key="list",
            uid="",
            entity=list_data,
            parent=root,
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="Bush"),
        )

        item_1_data = {"name": "Item1", "description": "", "type": "Garden"}
        item_1 = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="0",
            uid="",
            entity=item_1_data,
            blueprint_provider=BlueprintProvider.get_blueprint,
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

        self.assertEqual(actual_nested, tree_node_to_dict(nested))

        item_1_actual = {"name": "Item1", "description": "", "type": "Garden"}

        self.assertEqual(item_1_actual, tree_node_to_dict(item_1))

    def test_tree_node_to_ref_dict_2(self):
        input_entity = {
            "type": "dmss://system/SIMOS/Reference",
            "referenceType": "link",
            "address": "dmss://DemoDataSource/$product1",
        }
        a_nested_object = ({"type": "system/SIMOS/NamedEntity", "name": "nested obj", "description": "a description"},)
        form_example_entity = {
            "_id": "formExample",
            "type": "FormBlueprint",
            "aNestedObject": a_nested_object,
            "inputEntity": input_entity,
        }
        form_example_blueprint_attribute = BlueprintAttribute(
            name="?",
            attribute_type="FormBlueprint",
            type="dmss://system/SIMOS/BlueprintAttribute",
            contained=True,
        )

        input_entity_attribute = BlueprintAttribute(
            name="?",
            attribute_type="dmss://system/SIMOS/Reference",
            type="dmss://system/SIMOS/BlueprintAttribute",
            contained=False,
        )
        a_nested_object_attribute = BlueprintAttribute(
            name="?",
            attribute_type="dmss://system/SIMOS/NamedEntity",
            type="dmss://system/SIMOS/BlueprintAttribute",
            contained=True,
        )

        input_entity_node = Node(
            key="inputEntity",
            entity=input_entity,
            attribute=input_entity_attribute,
            blueprint_provider=mock_document_service.get_blueprint,
            recipe_provider=mock_storage_recipe_provider,
        )
        a_nested_object_node = Node(
            key="aNestedObject",
            entity=a_nested_object,
            attribute=a_nested_object_attribute,
            blueprint_provider=mock_document_service.get_blueprint,
            recipe_provider=mock_storage_recipe_provider,
        )

        form_node = Node(
            key="",
            entity=form_example_entity,
            attribute=form_example_blueprint_attribute,
            blueprint_provider=mock_document_service.get_blueprint,
            recipe_provider=mock_storage_recipe_provider,
        )
        form_node.children = [a_nested_object_node, input_entity_node]

        # Act
        form_dict = tree_node_to_ref_dict(form_node)

        # Assert
        assert form_dict["inputEntity"] == {
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
            "address": "dmss://DemoDataSource/$product1",
        }
        # Check that optional attributes that don't exist on the node entity are not added by tree_node_to_ref_dict()
        assert "aOptionalNestedObject" not in form_node.entity and "aOptionalNestedObject" not in form_dict

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
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="uncontained_list_blueprint"),
        )
        uncontained_in_every_way_node = ListNode(
            recipe_provider=mock_storage_recipe_provider,
            key="uncontained_in_every_way",
            uid="1.uncontained_in_every_way",
            entity=uncontained_in_every_way,
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )
        reference_1_node = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="0",
            uid="1.uncontained_in_every_way.0",
            entity=reference_1,
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="dmss://system/SIMOS/Reference"),
        )
        reference_2_node = Node(
            recipe_provider=mock_storage_recipe_provider,
            key="1",
            uid="1.uncontained_in_every_way.1",
            entity=reference_2,
            blueprint_provider=BlueprintProvider.get_blueprint,
            attribute=BlueprintAttribute(name="", attribute_type="dmss://system/SIMOS/Reference"),
        )
        uncontained_in_every_way_node.children.append(reference_1_node)
        uncontained_in_every_way_node.children.append(reference_2_node)
        parent_node.children.append(uncontained_in_every_way_node)
        parent_document = tree_node_to_ref_dict(parent_node)
        assert parent_document["uncontained_in_every_way"][0] == reference_1
        assert parent_document["uncontained_in_every_way"][1] == reference_2


if __name__ == "__main__":
    unittest.main()
