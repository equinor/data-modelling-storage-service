from collections.abc import Callable
from copy import deepcopy
from typing import Any

from common.exceptions import (
    BadRequestException,
    ValidationException,
)
from common.tree.tree_node import ListNode, Node
from common.utils.logging import logger
from config import config
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import StorageRecipe
from enums import REFERENCE_TYPES, SIMOS, BuiltinDataTypes


def tree_node_to_dict(node: Node | ListNode) -> list[Any] | dict:
    if node.is_array():
        return [tree_node_to_dict(child) for child in node.children]

    data = {}

    # If it's an empty node, just return the empty object.
    if not node.entity:
        return node.entity

    # Always add 'type'
    try:
        data["type"] = node.entity["type"]
    except KeyError as ex:
        raise BadRequestException(f"The node '{node.uid}' is missing the 'type' attributes") from ex

    if node.uid and not data["type"] == SIMOS.REFERENCE.value:
        data["_id"] = node.uid

    # Primitive
    # if complex attribute name is renamed in blueprint, then the blueprint is None in the entity.
    if node.blueprint is not None:
        for attribute in node.blueprint.get_primitive_types():
            if attribute.name in node.entity:
                data[attribute.name] = node.entity[attribute.name]

    # Complex
    for node_child in node.children:
        if node_child.is_array():
            data[node_child.key] = [tree_node_to_dict(child) for child in node_child.children]
        else:
            data[node_child.key] = tree_node_to_dict(node_child)

    return data


def _create_storage_reference_to_node(node: Node):
    if not node.uid:
        node.uid = node.generate_id()
    return {
        "type": SIMOS.REFERENCE.value,
        "address": f"${node.uid}",
        "referenceType": REFERENCE_TYPES.STORAGE.value,
    }


# flake8: noqa: C901
def tree_node_to_ref_dict(node: Node | ListNode) -> dict:
    """
    Rebuilds the entity as it should be stored based on the passed child entities that can be either contained
    documents, or references.
    """
    if not node.entity:
        return {}
    data = {}
    if node.uid and node.type != SIMOS.REFERENCE.value:
        data = {"_id": node.uid}

    # Always add 'type', regardless of blueprint
    try:
        data["type"] = node.type
    except KeyError as ex:
        raise BadRequestException(f"The node '{node.uid}' is missing the 'type' attributes") from ex

    if node.attribute.attribute_type == BuiltinDataTypes.BINARY.value:
        # Just return the reference, because binary data is uncontained and should not be resolved.
        return node.entity

    # Primitive
    # if complex attribute name is renamed in blueprint, then the blueprint is None in the entity.
    if node.attribute.attribute_type != BuiltinDataTypes.BINARY.value and node.blueprint is not None:
        for attribute in node.blueprint.get_primitive_types():
            if attribute.name in node.entity:
                data[attribute.name] = node.entity[attribute.name]

    # Add _meta_ attribute if it exists in the entity
    if "_meta_" in node.entity:
        data["_meta_"] = node.entity["_meta_"]

    # Complex
    for child in node.children:
        if child.is_array():
            # If the content of the list is not contained, i.e. references.
            if not child.storage_contained:
                data[child.key] = []
                for item in child.children:
                    data[child.key].append(
                        _create_storage_reference_to_node(item) if item.type != SIMOS.REFERENCE.value else item.entity
                    )
            else:
                data[child.key] = [tree_node_to_ref_dict(list_child) for list_child in child.children]
        else:
            if not child.storage_contained:
                data[child.key] = (
                    _create_storage_reference_to_node(child) if child.type != SIMOS.REFERENCE.value else child.entity
                )
            else:
                data[child.key] = tree_node_to_ref_dict(child)
    return data


def tree_node_from_dict(
    entity: dict,
    blueprint_provider: Callable[[str], Blueprint],
    node_attribute: BlueprintAttribute | None = None,
    recursion_depth: int = 0,
    recipe_provider: Callable[..., list[StorageRecipe]] | None = None,
    uid: str | None = None,
    key: str | None = None,
    data_source: str | None = None,
) -> Node:
    if recursion_depth >= config.MAX_ENTITY_RECURSION_DEPTH:
        message = (
            f"Reached maximum recursion depth while creating NodeTree ({recursion_depth}).\n"
            f'If your blueprints contains recursion, set the attribute as "optional". '
        )
        logger.error(message)
        raise RecursionError(message)

    # If no attribute, that means this was a "top-level" entity. We create an Attribute based on the Blueprint
    if not node_attribute:
        bp = blueprint_provider(entity["type"])
        node_attribute = BlueprintAttribute(name=bp.name, attributeType=entity["type"], description=bp.description)

    # If there is data in the entity, load attribute type from the entity
    if entity:
        if not entity.get("type"):
            raise ValueError(f"Entity is missing required attribute 'type'.\n{key}\n{entity}")
        node_attribute = deepcopy(node_attribute)  # If you don't copy, we modify the blueprint in the BP Cache...
        node_attribute.attribute_type = entity["type"]

    key = key if key else node_attribute.name
    node = Node(
        key=key,
        uid=uid,
        entity=entity,
        data_source=data_source,
        blueprint_provider=blueprint_provider,
        attribute=node_attribute,
        recipe_provider=recipe_provider,
    )

    if node.attribute.attribute_type == BuiltinDataTypes.BINARY.value:
        return node

    for child_attribute in node.blueprint.get_none_primitive_types():
        if child_attribute.name == "_meta_":
            continue
        if child_attribute.name == "default" and child_attribute.attribute_type == "any":
            continue
        # This will stop creation of recursive blueprints (only if they are optional)
        if child_attribute.is_optional and child_attribute.name not in entity:
            continue

        if child_attribute.is_array:
            children = entity.get(child_attribute.name, [])

            if not isinstance(children, list):
                raise ValueError(
                    f"The attribute '{child_attribute.name}' on blueprint '{node.type}' "
                    + f"should be a list, but was '{type(children)}'"
                )

            list_node = ListNode(
                key=child_attribute.name,
                uid="",
                entity=children,
                blueprint_provider=blueprint_provider,
                recipe_provider=recipe_provider,
                attribute=child_attribute,
            )

            for i, child in enumerate(children):
                list_child_attribute = deepcopy(child_attribute)

                # If the node is of type DMT/Package, we need to override the attribute_type "Entity",
                # and get it from the child.
                if node.type == SIMOS.PACKAGE.value:
                    content_attribute: BlueprintAttribute = deepcopy(child_attribute)
                    content_attribute.attribute_type = child["type"]
                    list_child_attribute = content_attribute

                # The child inside a list is identical to the attribute in the parent,
                # except it does not have dimensions *
                list_child_attribute.dimensions.dimensions = ""

                list_child_node = tree_node_from_dict(
                    uid=None if child["type"] == SIMOS.REFERENCE.value else child.get("_id", ""),
                    entity=child,
                    key=str(i),
                    blueprint_provider=blueprint_provider,
                    recipe_provider=recipe_provider,
                    node_attribute=list_child_attribute,
                    recursion_depth=recursion_depth + 1,
                )
                list_node.add_child(list_child_node)
            node.add_child(list_node)
        else:
            attribute_data = entity.get(child_attribute.name, {})
            if not isinstance(attribute_data, dict):
                raise ValidationException(
                    f"The attribute '{child_attribute.name}' on blueprint '{node.type}' "
                    + f"should be a dict, but was '{type(attribute_data)}'"
                )

            child_node = tree_node_from_dict(
                uid=None if attribute_data.get("type", "") == SIMOS.REFERENCE.value else attribute_data.get("_id", ""),
                entity=attribute_data,
                key=child_attribute.name,
                blueprint_provider=blueprint_provider,
                recipe_provider=recipe_provider,
                node_attribute=child_attribute,
                recursion_depth=recursion_depth + 1,
            )
            node.add_child(child_node)

    return node
