from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_data.mock_document_service import get_mock_document_service
from tests.unit.mock_data.mock_recipe_provider import mock_storage_recipe_provider
from tests.unit.test_tree_functionality.blueprints_for_tree_tests import get_blueprint


def get_engine_package_node() -> Node:
    """return a Node object for engine package that contains a single Bluepring called Engine."""
    document_service = get_mock_document_service()

    # Engine is a blueprint in a package called EnginePackage.
    # We need to create 3 nodes: engine package, content list in engine package and the engine.
    engine_entity = {
        "name": "Engine",
        "type": "dmss://system/SIMOS/Blueprint",
        "extends": ["dmss://system/SIMOS/NamedEntity"],
        "attributes": [{"name": "hp", "type": "dmss://system/SIMOS/BlueprintAttribute", "attributeType": "string"}],
    }
    engine_blueprint_attribute = BlueprintAttribute(
        name="content",
        attribute_type=SIMOS.REFERENCE.value,
        type="dmss://system/SIMOS/BlueprintAttribute",
        contained=False,
    )
    engine_package_content_bp_attribute = BlueprintAttribute(
        name="content", attribute_type="object", type="dmss://system/SIMOS/BlueprintAttribute"
    )
    engine_entity_ref = {"address": "$123", "type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value}

    engine_package_content: ListNode = ListNode(
        key="content",
        attribute=engine_package_content_bp_attribute,
        entity=[engine_entity_ref],
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
    )

    engine_ref_node = Node(
        key="0",
        entity=engine_entity_ref,
        attribute=engine_blueprint_attribute,
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
        uid=engine_entity_ref["address"],
    )

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
    engine_package_node: Node = Node(
        key="Package",
        entity=engine_package_entity,
        attribute=engine_package_blueprint_attribute,
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
    )

    """
    Node structure:
    * EnginePackage
        * content list
            * engine reference
    """
    engine_package_content.parent = engine_package_node
    engine_package_node.children = [engine_package_content]
    engine_package_content.children = [engine_ref_node]
    engine_ref_node.parent = engine_package_content.children[0]
    return engine_package_node


def get_form_example_node() -> Node:
    document_service = get_mock_document_service()

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
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
    )
    a_nested_object_node = Node(
        key="aNestedObject",
        entity=a_nested_object,
        attribute=a_nested_object_attribute,
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
    )

    form_node = Node(
        key="",
        entity=form_example_entity,
        attribute=form_example_blueprint_attribute,
        blueprint_provider=get_blueprint,
        recipe_provider=mock_storage_recipe_provider,
    )
    form_node.children = [a_nested_object_node, input_entity_node]
    return form_node
