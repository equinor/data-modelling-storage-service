import unittest

from common.tree_node_serializer import tree_node_to_ref_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.get_node_for_tree_tests import (
    get_form_example_node,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_blueprint_provider_for_tree_tests import (
    BlueprintProvider,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_document_service_for_tree_tests import (
    mock_document_service,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_storage_recipe_provider import (
    mock_storage_recipe_provider,
)


class TreeNodeToRefDictTestCase(unittest.TestCase):
    def test_tree_node_to_ref_dict(self):
        # Arrange
        engine_package_content_bp_attribute = BlueprintAttribute(
            name="content", attribute_type="object", type="dmss://system/SIMOS/BlueprintAttribute"
        )
        engine_entity_ref = {
            "address": "$123",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

        engine_package_entity = {
            "_id": "26d94353-3ff0-4b7d-bf06-86f006dd6f7b",
            "type": "dmss://system/SIMOS/Package",
            "name": "EnginePackage",
            "isRoot": False,
            "content": [engine_entity_ref],
        }
        engine_package_blueprint_attribute = BlueprintAttribute(
            name="Package",
            attribute_type="dmss://system/SIMOS/Package",
            type="dmss://system/SIMOS/BlueprintAttribute",
        )
        engine_package_node = Node(
            key="Package",
            entity=engine_package_entity,
            attribute=engine_package_blueprint_attribute,
            blueprint_provider=mock_document_service.get_blueprint,
            recipe_provider=None,
        )

        engine_blueprint_attribute = BlueprintAttribute(
            name="content",
            attribute_type=SIMOS.REFERENCE.value,
            type="dmss://system/SIMOS/BlueprintAttribute",
            contained=False,
        )
        engine_ref_node = Node(
            key="0",
            entity=engine_entity_ref,
            attribute=engine_blueprint_attribute,
            blueprint_provider=mock_document_service.get_blueprint,
            recipe_provider=None,
            uid=engine_entity_ref["address"],
        )

        content = ListNode(
            key="content",
            attribute=engine_package_content_bp_attribute,
            entity=[engine_entity_ref],
            blueprint_provider=None,
            recipe_provider=None,
        )
        content.children = [engine_ref_node]
        engine_package_node.children = [content]

        content.parent = engine_package_node
        engine_ref_node.parent = content.children[0]

        # Act
        engine_package_dict = tree_node_to_ref_dict(engine_package_node)

        # Assert
        assert engine_package_dict["content"][0] == {
            "address": "$123",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
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
