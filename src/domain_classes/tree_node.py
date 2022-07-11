from copy import deepcopy
from typing import Dict, List, Optional, Union
from uuid import uuid4


from config import config
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import StorageAttribute
from enums import BuiltinDataTypes, SIMOS, StorageDataTypes
from utils.exceptions import InvalidChildTypeException, InvalidEntityException
from utils.logging import logger
from utils.validators import valid_extended_type


class DictExporter:
    @staticmethod
    def to_dict(node):
        data = {}

        # If it's an empty node, just return the empty object.
        if not node.entity:
            return node.entity

        if node.uid:
            data["_id"] = node.uid

        # Always add 'type'
        try:
            data["type"] = node.entity["type"]
        except KeyError:
            raise InvalidEntityException(f"The node '{node.uid}' is missing the 'type' attributes")
        # Primitive
        # if complex attribute name is renamed in blueprint, then the blueprint is None in the entity.
        if node.blueprint is not None:
            for attribute in node.blueprint.get_primitive_types():
                if attribute.name in node.entity:
                    data[attribute.name] = node.entity[attribute.name]

        # Complex
        for node in node.children:
            if node.is_array():
                data[node.key] = [child.to_dict() for child in node.children]
            else:
                data[node.key] = node.to_dict()

        return data

    @staticmethod
    def to_ref_dict(node):
        """
        Rebuilds the entity as it should be stored based on the passed child entities that can be either contained
        documents, or references.
        """
        if node.is_empty():
            return node.entity
        data = {}
        if node.uid:
            data = {"_id": node.uid}

        # Always add 'type', regardless of blueprint
        try:
            data["type"] = node.type
        except KeyError:
            raise InvalidEntityException(f"The node '{node.uid}' is missing the 'type' attributes")

        # Primitive
        # if complex attribute name is renamed in blueprint, then the blueprint is None in the entity.
        if node.blueprint is not None:
            for attribute in node.blueprint.get_primitive_types():
                if attribute.name in node.entity:
                    data[attribute.name] = node.entity[attribute.name]

        # Complex
        for child in node.children:
            if child.is_array():
                # If the content of the list is not contained, i.e. references.
                if not child.storage_contained:
                    data[child.key] = [
                        {"_id": child.uid, "type": child.type, "name": child.name, "contained": child.contained}
                        for child in child.children
                    ]
                else:
                    data[child.key] = [list_child.to_ref_dict() for list_child in child.children]
            else:
                if not child.contained and child.entity:
                    data[child.key] = {
                        "_id": child.uid,
                        "type": child.type,
                        "name": child.name,
                        "contained": child.contained,
                    }
                else:
                    data[child.key] = child.to_ref_dict()
        return data


class DictImporter:
    @classmethod
    def from_dict(cls, entity, uid, blueprint_provider, key=None, node_attribute: BlueprintAttribute = None):
        return cls._from_dict(entity, uid, key, blueprint_provider, node_attribute)

    @classmethod
    def _from_dict(
        cls,
        entity: Union[dict, list],
        uid: str,
        key,
        blueprint_provider,
        node_attribute: BlueprintAttribute = None,
        recursion_depth: int = 0,
    ):

        if recursion_depth >= config.MAX_ENTITY_RECURSION_DEPTH:
            message = (
                f"Reached maximum recursion depth while creating NodeTree ({recursion_depth}).\n"
                f"Node: {node_attribute.name}, Type: {node_attribute.attribute_type}\n"
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
        node = Node(key=key, uid=uid, entity=entity, blueprint_provider=blueprint_provider, attribute=node_attribute)

        for child_attribute in node.blueprint.get_none_primitive_types():
            child_contained = node.blueprint.storage_recipes[0].is_contained(child_attribute.name)
            # This will stop creation of recursive blueprints (only if they are optional)
            if child_attribute.is_optional() and not entity:
                continue

            if child_attribute.is_array():
                children = entity.get(child_attribute.name, [])

                if not isinstance(children, list):
                    raise ValueError(
                        f"The attribute '{child_attribute.name}' on blueprint '{node.type}' "
                        + f"should be a list, but was '{str(type(children))}'"
                    )

                list_node = ListNode(
                    key=child_attribute.name,
                    uid="",
                    entity=children,
                    blueprint_provider=blueprint_provider,
                    attribute=child_attribute,
                )

                for i, child in enumerate(children):
                    list_child_attribute = child_attribute

                    # If the node is of type DMT/Package, we need to override the attribute_type "Entity",
                    # and get it from the child.
                    if node.type == SIMOS.PACKAGE.value:
                        content_attribute: BlueprintAttribute = deepcopy(child_attribute)
                        content_attribute.attribute_type = child["type"]
                        list_child_attribute = content_attribute

                    list_child_node = cls._from_dict(
                        uid=child.get("_id", ""),
                        entity=child,
                        key=str(i),
                        blueprint_provider=blueprint_provider,
                        node_attribute=list_child_attribute,
                        recursion_depth=recursion_depth + 1,
                    )
                    list_node.add_child(list_child_node)
                node.add_child(list_node)
            else:
                attribute_data = entity.get(child_attribute.name, {})
                if not isinstance(attribute_data, dict):
                    raise ValueError(
                        f"The attribute '{child_attribute.name}' on blueprint '{node.type}' "
                        + f"should be a dict, but was '{str(type(attribute_data))}'"
                    )
                child_node = cls._from_dict(
                    # If the child is not contained, get or create it's _id
                    uid="" if child_contained or not attribute_data else attribute_data.get("_id", ""),
                    entity=attribute_data,
                    key=child_attribute.name,
                    blueprint_provider=blueprint_provider,
                    node_attribute=child_attribute,
                    recursion_depth=recursion_depth + 1,
                )
                node.add_child(child_node)

        return node


class NodeBase:
    def __init__(
        self,
        key: str,
        attribute: BlueprintAttribute,
        uid: str = None,
        parent=None,
        blueprint_provider=None,
        children=None,
        entity: dict = {},
    ):
        if key is None:
            raise Exception("Node requires a key")
        self.key = key
        self.attribute = attribute
        self.type = self.attribute.attribute_type
        self.uid = uid
        self.entity = entity
        self.parent: Union[Node, ListNode] = parent
        if parent:
            parent.add_child(self)
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        self.blueprint_provider = blueprint_provider
        self.has_error = False

    @property
    def type(self):
        return self._type

    @property
    def blueprint(self) -> Optional[Blueprint]:
        if self.type == BuiltinDataTypes.OBJECT.value:
            return self.blueprint_provider(SIMOS.ENTITY.value)
        if self.type != "datasource":
            return self.blueprint_provider(self.type)

    @type.setter
    def type(self, value):  # Type can be changed after initiation. e.g Multiple valid specialised types
        self._type = value

    def is_empty(self):
        return not self.entity

    @property
    def parent_node_id(self):
        if not self.parent:
            return None

        return self.parent.node_id

    @property
    def storage_contained(self):
        if not self.parent or self.parent.type == SIMOS.DATASOURCE.value:
            return False
        return self.parent.blueprint.storage_recipes[0].is_contained(self.attribute.name)

    @property
    def contained(self):
        return self.attribute.contained

    @property
    def node_id(self):
        """
        When a node is accessed through a parent,
        only contained attributes with none-contained storage return UUID,
        the rest return dotted path
        """
        if self.type == SIMOS.DATASOURCE.value:
            return self.uid
        if not self.parent:
            return self.uid
        if self.contained and not self.storage_contained and not self.is_array():
            return self.uid
        return ".".join((self.parent.node_id, self.key))

    def path(self):
        path = []
        parent = self.parent
        while parent:  # Build the path from Node.key until the node has no key (root node)
            path += [parent.key] if parent.key else [parent.uid]
            parent = parent.parent
        # Since we build the path "bottom-up", it need's to be revered.
        # eg. [parent, grand_parent, grand_grand_parent]
        path.reverse()
        return path

    def traverse(self):
        """Iterate in pre-order depth-first search order (DFS)"""
        yield self

        # first, yield everything every one of the child nodes would yield.
        for child in self.children:
            for item in child.traverse():
                # the two for loops is because there's multiple children,
                # and we need to iterate over each one.
                yield item

    def traverse_reverse(self):
        """Iterate up the tree"""
        node = self
        while node is not None:
            yield node
            node = node.parent

    def __repr__(self):
        return f"Name: '{self.name}', Key: '{self.key}', Type: '{self.type}', Node_ID: '{self.node_id}'"

    def show_tree(self, level=0):
        print("%s%s" % ("." * level, self))
        for node in self.children:
            node.show_tree(level + 2)

    def is_array(self):
        return isinstance(self, ListNode)

    def is_complex_array(self):
        return self.attribute.is_matrix()

    def is_single(self):
        return isinstance(self, Node)

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def depth(self):
        """Depth of current node"""
        if self.is_root():
            return 0
        else:
            return 1 + self.parent.depth()

    def search(self, node_id: str):
        if self.node_id == node_id:
            return self
        for node in self.traverse():
            if node.node_id == node_id:
                return node
        return None

    def replace(self, node_id, new_node):
        for node in self.traverse():
            for i, n in enumerate(node.children):
                if n.node_id == node_id:
                    new_node.parent = node
                    node.children[i] = new_node

    def has_children(self):
        return len(self.children) > 0

    def contains(self, name: str):
        keys = [child.key for child in self.children]
        return name in keys

    def get_by_path(self, keys: List[str]):
        if len(keys) == 0:
            return self

        next_node = next((x for x in self.children if x.key == keys[0]), None)
        if not next_node:
            return
        keys.pop(0)
        next_node = next_node.get_by_path(keys)
        return next_node

    def get_by_name_path(self, path: List):
        if len(path) == 0:
            return self

        next_node = next((x for x in self.children if x.name == path[0]), None)
        if not next_node:
            return
        path.pop(0)
        next_node = next_node.get_by_name_path(path)
        return next_node

    def remove_by_path(self, keys: List) -> None:
        if len(keys) == 1:
            for index, child in enumerate(self.children):
                if child.key == keys[0]:
                    self.children.pop(index)
                    return
            return
        next_node = next((x for x in self.children if x.key == keys[0]), None)
        if not next_node:
            return
        keys.pop(0)
        next_node.remove_by_path(keys)

    def remove(self):
        self.parent.remove_by_child_id(self.node_id)

    def remove_by_child_id(self, node_id) -> None:
        for i, c in enumerate(self.children):
            if c.node_id == node_id:
                self.children.pop(i)

    def has_error(self):
        return self.error is not None

    def duplicate_attribute(self, attribute: str):
        if next((child for child in self.children if child.name == attribute), None):
            return True

    def validate_type_on_parent(self):
        if not self.parent:
            return True
        key = self.key if not self.parent.is_array() else self.parent.key  # Use attribute key, not list index
        valid_type = self.parent.blueprint.get_attribute_type_by_key(key)  # Valid type as defined in parents blueprint
        if not valid_extended_type(
            valid_type, [self.type] + self.blueprint.extends, self.blueprint_provider
        ):  # Resolve extends
            raise InvalidChildTypeException(self.type, key, valid_type)


class Node(NodeBase):
    def __init__(
        self,
        key: str,  # The key this node is in parent
        attribute: BlueprintAttribute,  # The BlueprintAttribute this Node is in parent
        uid: str = None,
        entity: Dict = {},
        parent=None,
        blueprint_provider=None,
    ):
        super().__init__(key, attribute, uid, parent, blueprint_provider, entity=entity)
        self.error_message = None

    def is_root(self):
        return super().is_root()

    def to_dict(self):
        return DictExporter.to_dict(self)

    def to_ref_dict(self):
        return DictExporter.to_ref_dict(self)

    @property
    def name(self):
        return self.entity.get("name", self.attribute.name)

    @staticmethod
    def from_dict(entity, uid, blueprint_provider, node_attribute: BlueprintAttribute = None):
        return DictImporter.from_dict(entity, uid, blueprint_provider, "", node_attribute)

    def set_error(self, error_message: str):
        self.has_error = True
        self.error_message = error_message

    # Replace the entire data of the node with the input dict. If it matches the blueprint...
    def update(self, data: dict):

        self.set_uid(data.get("_id"))
        # Set self.type from posted type, and validate against parent blueprint
        self.type = data.get("type", self.attribute.attribute_type)
        self.validate_type_on_parent()

        # Modify and add for each key in posted data
        for key in data.keys():
            if key == "_id":
                continue
            new_data = data[key]
            attribute = self.blueprint.get_attribute_by_name(key)
            if not attribute:  # This skips adding any attribute that is not specified in the blueprint
                continue

            # Add/Modify primitive data
            if attribute.is_primitive():
                self.entity[key] = new_data
            # Add/Modify complex data
            else:
                child = self.get_by_path([key])
                if not child:  # A new child has been added
                    if attribute.is_array():
                        child = ListNode(attribute.name, attribute, None, new_data, self, self.blueprint_provider)
                    else:
                        child = Node(attribute.name, attribute, None, new_data, self, self.blueprint_provider)
                child.update(new_data)

        # Remove for every key in blueprint not in data or is a required attribute
        removed_attributes = [attr for attr in self.blueprint.attributes if attr.name not in data]
        for attribute in removed_attributes:
            # Pop primitive data
            if attribute.is_primitive():
                self.entity.pop(attribute.name, None)
            # Remove complex data
            else:
                self.remove_by_path([attribute.name])

    def get_context_storage_attribute(self):
        # TODO: How to decide which storage_recipe?
        if self.parent and self.parent.type != SIMOS.DATASOURCE.value:
            # The 'node.attribute.name' will be invalid for Package.content. Set it explicitly
            nodes_attribute_on_parent = (
                self.attribute.name if not self.parent.type == BuiltinDataTypes.OBJECT.value else "content"
            )
            storage_attribute = self.parent.blueprint.storage_recipes[0].storage_attributes[nodes_attribute_on_parent]

            # If the attribute has default StorageAffinity in the parent, get it from the nodes own storageRecipe
            if storage_attribute.storage_type_affinity is StorageDataTypes.DEFAULT:
                storage_attribute.storage_type_affinity = self.blueprint.storage_recipes[0].storage_affinity
            return storage_attribute
        # If no parent, the node is always contained, and get storageAffinity from the nodes own storageRecipe
        return StorageAttribute(
            name=self.type, contained=True, storageTypeAffinity=self.blueprint.storage_recipes[0].storage_affinity
        )

    def set_uid(self, new_id: str = None):
        """
        Based on storage contained, sets, or removes the documents uid. Creates new if missing.
        """
        if not self.entity and not new_id:
            return

        if self.storage_contained:
            self.uid = None
            self.entity.pop("_id", None)
            return

        current_id = new_id if new_id else self.entity.get("_id", self.uid if self.uid else str(uuid4()))
        self.uid = current_id
        self.entity["_id"] = self.uid


class ListNode(NodeBase):
    def __init__(
        self,
        key: str,
        attribute: BlueprintAttribute,
        uid: str = None,
        entity: Dict = {},
        parent=None,
        blueprint_provider=None,
    ):
        super().__init__(key, attribute, uid, parent=parent, blueprint_provider=blueprint_provider, entity=entity)

    def to_dict(self):
        return [child.to_dict() for child in self.children]

    @property
    def name(self):
        return self.attribute.name

    @property
    def blueprint(self):
        return self.parent.blueprint

    def update(self, data: list):
        self.children = []
        for i, item in enumerate(data):
            # Set self.type from posted type, and validate against parent blueprint
            self.type = item["type"]
            self.validate_type_on_parent()

            # Set uid base on containment and existing(lack of) uid
            # This require the existing _id to be posted
            uid = "" if self.storage_contained else item.get("_id", str(uuid4()))
            self.add_child(
                DictImporter.from_dict(entity=item, uid=uid, blueprint_provider=self.blueprint_provider, key=str(i))
            )
