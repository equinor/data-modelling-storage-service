from collections.abc import Callable
from uuid import uuid4

from common.exceptions import ValidationException
from common.providers.storage_recipe_provider import create_default_storage_recipe
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from enums import SIMOS, BuiltinDataTypes, StorageDataTypes


class NodeBase:
    def __init__(
        self,
        key: str,
        attribute: BlueprintAttribute,
        uid: str | None = None,
        parent=None,
        blueprint_provider=None,
        children=None,
        entity: dict | list[dict] | None = None,
        recipe_provider: Callable[..., list[StorageRecipe]] | None = None,
    ):
        if key is None:
            raise Exception("Node requires a key")
        self.key = key
        self.attribute = attribute
        self._type = self.attribute.attribute_type
        self.uid = uid
        self.entity = entity if entity else {}
        self.parent: Node | ListNode = parent
        if parent:
            parent.add_child(self)
        self.children: list[Node | ListNode] = []
        if children is not None:
            for child in children:
                self.add_child(child)
        self.blueprint_provider = blueprint_provider
        self.recipe_provider = recipe_provider

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):  # Type can be changed after initiation. e.g Multiple valid specialised types
        self._type = value

    @property
    def is_optional(self):
        if not self.parent:
            return True
        if self.parent.is_array():
            return True
        return self.attribute.is_optional

    @property
    def blueprint(self) -> Blueprint:
        if self.type == BuiltinDataTypes.OBJECT.value:
            return self.blueprint_provider(SIMOS.ENTITY.value)
        if self.type != "datasource":
            return self.blueprint_provider(self.type)

    @property
    def storage_recipes(self, context: str | None = "DMSS") -> list[StorageRecipe]:
        # TODO: support other contexts than "DMSS"
        if not self.recipe_provider or not (context_recipes := self.recipe_provider(self.type, context)):
            return create_default_storage_recipe()
        return context_recipes

    @property
    def storage_contained(self):
        if not self.parent or self.parent.type == SIMOS.DATASOURCE.value:
            return False
        if self.parent.is_array():
            return self.parent.parent.storage_recipes[0].is_contained(self.parent.attribute.name)
        if self.parent.storage_recipes:
            return self.parent.storage_recipes[0].is_contained(self.attribute.name)
        return True

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
        if not self.storage_contained and not self.is_array():
            return self.uid
        if self.parent.is_array():
            if self.attribute.ensure_uid:
                return f'{self.parent.node_id}(_id="{self.uid}")'

            return f"{self.parent.node_id}[{self.key}]"
        return ".".join((self.parent.node_id, self.key))

    def path(self):
        path = []
        parent = self.parent
        while parent:  # Build the path from Node.key until the node has no key (root node)
            path += [parent.key] if parent.key else [parent.uid]  # type: ignore
            parent = parent.parent
        # Since we build the path "bottom-up", it needs to be revered.
        # e.g. [parent, grand_parent, grand_grand_parent]
        path.reverse()
        return path

    def traverse(self):
        """Iterate in pre-order depth-first search order (DFS)"""
        yield self

        # first, yield everything every one of the child nodes would yield.
        for child in self.children:
            yield from child.traverse()

    def traverse_reverse(self):
        """Iterate up the tree"""
        node = self
        while node is not None:
            yield node
            node = node.parent

    def find_parent(self):
        nodes = list(self.traverse_reverse())
        if len(nodes) > 1:
            nodes.pop(0)  # Remove first node since parent of self cannot be self
        for node in nodes:
            if not node.storage_contained and not isinstance(node, ListNode):
                return node

    def __repr__(self):
        return f"Key: '{self.key}', Type: '{self.type}', Node_ID: '{self.node_id}'"

    def show_tree(self, level=0):
        print(f"{'.' * level}{self}")
        for node in self.children:
            node.show_tree(level + 2)

    def is_array(self):
        return isinstance(self, ListNode)

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def depth(self):
        """Depth of current node"""
        if self.parent is None:
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

    def get_by_path(self, keys: list[str]):
        """
        Uses a list of keys to find and return the correct child node

        :param keys: list of keys, ex ["[0]", "cars", "0", "engine"]. Keys on format "cars[0]" are invalid
        """
        if len(keys) == 0:
            return self

        next_node = next((x for x in self.children if x.key == keys[0].strip("[]")), None)
        if not next_node:
            return
        keys.pop(0)
        next_node = next_node.get_by_path(keys)
        return next_node

    def remove_by_path(self, keys: list) -> None:
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

    def duplicate_attribute(self, attribute: str):
        if next(
            (child for child in self.children if child.entity.get("name", self.attribute.name) == attribute),  # type: ignore
            None,
        ):
            return True

    def should_have_id(self):
        if self.attribute.ensure_uid:
            return True
        if isinstance(self, ListNode):
            return False
        if self.type == SIMOS.REFERENCE.value:
            return False
        if self.storage_contained and self.contained:
            return False
        return True


class Node(NodeBase):
    def __init__(
        self,
        key: str,  # The key this node is in parent
        attribute: BlueprintAttribute,  # The BlueprintAttribute this Node is in parent
        uid: str | None = None,
        entity: dict | None = None,
        parent=None,
        blueprint_provider=None,
        recipe_provider: Callable[..., list[StorageRecipe]] | None = None,
        data_source: str | None = None,
    ):
        super().__init__(
            key,
            attribute,
            uid,
            parent,
            blueprint_provider,
            entity=entity,
            recipe_provider=recipe_provider,
        )
        self.data_source = data_source
        self.entity: dict = entity if entity else {}

    # Replace the entire data of the node with the input dict. If it matches the blueprint...
    def update(self, data: dict, partial_update: bool = False):
        if data.get("_id"):
            self.set_uid(data.get("_id"))

        # Set self.type from posted type, and validate against parent blueprint
        self.type = data.get("type", self.attribute.attribute_type)
        # Modify and add for each key in posted data
        for key in data.keys():
            new_data = data[key]
            if key == "_id":
                self.entity["_id"] = new_data
                continue
            attribute = self.blueprint.get_attribute_by_name(key)

            if key == "type":
                # Should always be able to specify type
                self.entity[key] = new_data

            # Add/Modify primitive data
            if attribute.is_primitive:
                self.entity[key] = new_data
            # Add/Modify complex data
            else:
                child = self.get_by_path([key])
                if not child:  # A new child has been added
                    if attribute.is_array:
                        child = ListNode(
                            attribute.name,
                            attribute,
                            None,
                            new_data,
                            self,
                            self.blueprint_provider,
                            recipe_provider=self.recipe_provider,
                        )
                    else:
                        child = Node(
                            attribute.name,
                            attribute,
                            None,
                            new_data,
                            self,
                            self.blueprint_provider,
                            recipe_provider=self.recipe_provider,
                        )
                child.update(new_data, partial_update)

        # Remove any child that is not specified in blueprint
        # (Can happen if we change the type, and the old node had some children)
        for child in self.children:
            if child.attribute.name not in self.blueprint.get_attribute_names():
                self.remove_by_path([child.key])

        # Remove for every key in blueprint not in data or is a required attribute
        removed_attributes = [attr for attr in self.blueprint.attributes if attr.name not in data]
        for attribute in removed_attributes:
            # Pop primitive data
            if attribute.is_primitive:
                self.entity.pop(attribute.name, None)  # type: ignore
            # Remove complex data
            else:
                if not partial_update:
                    self.remove_by_path([attribute.name])

    def get_context_storage_attribute(self):
        # TODO: How to decide which storage_recipe?
        if self.parent and self.parent.type != SIMOS.DATASOURCE.value:
            # The 'node.attribute.name' will be invalid for Package.content. Set it explicitly
            nodes_attribute_on_parent = (
                self.attribute.name if not self.parent.type == BuiltinDataTypes.OBJECT.value else "content"
            )
            if self.parent.is_array():
                storage_attribute = self.parent.parent.storage_recipes[0].attributes[nodes_attribute_on_parent]
            else:
                storage_attribute = self.parent.storage_recipes[0].attributes[nodes_attribute_on_parent]

            # If the attribute has default StorageAffinity in the parent, get it from the nodes own storageRecipe
            if storage_attribute.storage_affinity is StorageDataTypes.DEFAULT:
                storage_attribute.storage_affinity = self.storage_recipes[0].storage_affinity
            return storage_attribute
        # If no parent, the node is always contained, and get storageAffinity from the nodes own storageRecipe
        return StorageAttribute(
            name=self.type,
            contained=True,
            storage_affinity=self.storage_recipes[0].storage_affinity,
        )

    def generate_id(self):
        if self.entity.get("_id"):
            return self.entity.get("_id")
        if self.uid:
            return self.uid
        return str(uuid4())

    def set_uid(self, new_id: str | None = None):
        self.uid = new_id
        if new_id:
            self.entity["_id"] = new_id
        else:
            self.entity.pop("_id", None)

    def get_data_source(self) -> str:
        if self.data_source:
            return self.data_source
        return self.find_parent().get_data_source()


class ListNode(NodeBase):
    def __init__(
        self,
        key: str,
        attribute: BlueprintAttribute,
        uid: str | None = None,
        entity: list | None = None,
        parent=None,
        blueprint_provider=None,
        recipe_provider: Callable[..., list[StorageRecipe]] | None = None,
    ):
        entity = entity if entity else []
        super().__init__(
            key,
            attribute,
            uid,
            parent=parent,
            blueprint_provider=blueprint_provider,
            entity=entity,
            recipe_provider=recipe_provider,
        )

    @property
    def name(self):
        return self.attribute.name

    @property
    def blueprint(self):
        return self.blueprint_provider(self.attribute.attribute_type)  # TODO: blueprint_provider is required now...

    def update(self, data: list, partial_update: bool):
        # Replaces the whole list with the new one
        if not isinstance(data, list):
            raise ValidationException(f"Cannot replace a list with a dictionary. Got data: {data}")
        self.children = []
        for i, item in enumerate(data):
            # Set self.type from posted type, and validate against parent blueprint
            self.type = item["type"]

            # Set uid base on containment and existing(lack of) uid
            # This requires the existing _id to be posted
            uid = "" if self.storage_contained and self.contained else item.get("_id", str(uuid4()))
            child = Node(
                entity={},
                uid=uid,
                blueprint_provider=self.blueprint_provider,
                key=str(i),
                recipe_provider=self.recipe_provider,
                attribute=BlueprintAttribute(name=self.name, attributeType=self.type),
                parent=self,
            )
            child.update(item, partial_update)  # This will handle updating of children recursively
