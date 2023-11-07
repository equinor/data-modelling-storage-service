import unittest

from common.tree.tree_node import ListNode, Node
from common.tree.tree_node_serializer import tree_node_to_ref_dict
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.common.tree.mock_data.get_mock_nodes import get_form_example_node
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider


class TreeNodeToRefDictTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = [
            "dmss://system/SIMOS/Package",
            "dmss://system/SIMOS/Reference",
            "dmss://system/SIMOS/Entity",
            "dmss://system/SIMOS/NamedEntity",
        ]
        mock_blueprint_folder = "src/tests/unit/common/tree/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "uncontained_list_blueprint": "uncontained_list_blueprint.blueprint.json",
            "FormBlueprint": "FormBlueprint.blueprint.json",
        }
        self.form_node = get_form_example_node(mock_blueprint_folder, mock_blueprints_and_file_names, simos_blueprints)

        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        ).get_blueprint

    def test_tree_node_to_ref_dict(self):
        # Arrange
        engine_package_content_bp_attribute = BlueprintAttribute(
            name="content",
            attribute_type="object",
            type="dmss://system/SIMOS/BlueprintAttribute",
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
            blueprint_provider=self.mock_blueprint_provider,
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
            blueprint_provider=self.mock_blueprint_provider,
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
        self.assertDictEqual(
            engine_package_dict["content"][0],
            {
                "address": "$123",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
        )

    def test_tree_node_to_ref_dict_2(self):
        form_dict = tree_node_to_ref_dict(self.form_node)
        assert form_dict["inputEntity"] == {
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
            "address": "dmss://DemoDataSource/$product1",
        }
        # Check that optional attributes that don't exist on the node entity are not added by tree_node_to_ref_dict()
        assert "aOptionalNestedObject" not in self.form_node.entity
        assert "aOptionalNestedObject" not in form_dict

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
            key="",
            uid="1",
            entity=document,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="uncontained_list_blueprint"),
        )
        uncontained_in_every_way_node = ListNode(
            key="uncontained_in_every_way",
            uid="1.uncontained_in_every_way",
            entity=uncontained_in_every_way,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="Garden"),
        )
        reference_1_node = Node(
            key="0",
            uid="1.uncontained_in_every_way.0",
            entity=reference_1,
            blueprint_provider=self.mock_blueprint_provider,
            attribute=BlueprintAttribute(name="", attribute_type="dmss://system/SIMOS/Reference"),
        )
        reference_2_node = Node(
            key="1",
            uid="1.uncontained_in_every_way.1",
            entity=reference_2,
            blueprint_provider=self.mock_blueprint_provider,
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
