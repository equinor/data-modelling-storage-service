import pprint
from functools import lru_cache
from typing import BinaryIO, Callable, Dict, List, Union
from uuid import uuid4

from authentication.models import ACL
from common.exceptions import (
    ApplicationException,
    BadRequestException,
    MissingPrivilegeException,
    NotFoundException,
    ValidationException,
)
from common.tree_node_serializer import (
    tree_node_from_dict,
    tree_node_to_dict,
    tree_node_to_ref_dict,
)
from common.utils.build_complex_search import build_mongo_query
from common.utils.delete_documents import delete_document
from common.utils.get_blueprint import get_blueprint_provider
from common.utils.get_document_by_path import get_document_uid_by_path
from common.utils.get_resolved_document_by_id import get_complete_sys_document
from common.utils.get_storage_recipe import storage_recipe_provider
from common.utils.logging import logger
from common.utils.sort_entities_by_attribute import sort_dtos_by_attribute
from common.utils.string_helpers import split_dmss_ref
from common.utils.validators import entity_has_all_required_attributes
from config import config, default_user
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from domain_classes.tree_node import ListNode, Node
from enums import SIMOS, BuiltinDataTypes, StorageDataTypes
from restful.request_types.shared import Entity, Reference
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source
from storage.repositories.mongo import MongoDBClient
from storage.repositories.zip import ZipFileClient

pretty_printer = pprint.PrettyPrinter()


class DocumentService:
    def __init__(
        self,
        repository_provider=get_data_source,
        blueprint_provider=None,
        user=default_user,
        context: str = None,
        recipe_provider=None,
    ):
        self._blueprint_provider = blueprint_provider or get_blueprint_provider(user)
        self._recipe_provider: Callable[..., list[StorageRecipe]] = recipe_provider or storage_recipe_provider
        self.repository_provider = repository_provider
        self.user = user
        self.context = context

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        blueprint: Blueprint = self._blueprint_provider.get_blueprint(type)
        blueprint.realize_extends(self._blueprint_provider.get_blueprint)
        return blueprint

    def _create_default_storage_recipe(self, type: str) -> list[StorageRecipe]:
        blueprint_attributes = self.get_blueprint(type).attributes
        return [
            StorageRecipe(
                name="Default",
                storage_affinity=StorageDataTypes.DEFAULT.value,
                attributes={
                    a.name: StorageAttribute(name=a.name, contained=a.contained) for a in blueprint_attributes
                },
            )
        ]

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_storage_recipes(self, type: str, context: str | None = None) -> list[StorageRecipe]:
        if not context:
            return self._create_default_storage_recipe(type)

        # TODO: Support other contexts
        if context_recipes := self._recipe_provider(type, context=context):
            return context_recipes

        # No storage recipes created for contex. Creating defaults
        return self._create_default_storage_recipe(type)

    def invalidate_cache(self):
        logger.warning("Clearing blueprint cache")
        self.get_blueprint.cache_clear()
        self._blueprint_provider.invalidate_cache()

    def save_blob_data(self, node, repository) -> dict:
        """
        Updates the posted blob and unlink the binary file from the Node.
        Returns a system/SIMOS/Blob entity with the created id
        """
        if file := node.entity.get("_blob_"):  # If a file was posted with the same name as this blob, save it
            # Get or set the "_blob_id"
            node.entity["_blob_id"] = node.entity["_blob_id"] if node.entity.get("_blob_id") else str(uuid4())
            # Save it
            repository.update_blob(node.entity["_blob_id"], file)
            node.entity["size"] = file.seek(0, 2)  # Set the size of the blob
            # Remove the temporary key containing the File
            del node.entity["_blob_"]

        return node.entity

    def save(
        self,
        node: Union[Node, ListNode],
        data_source_id: str,
        repository=None,
        path="",
        update_uncontained: bool = False,
        combined_document_meta: dict | None = None,
    ) -> Dict:
        """
        Recursively saves a Node.
        Digs down to the leaf child, and based on storageContained,
        either saves the entity and returns the Reference, OR returns the entire entity.

        combined_document_meta is the combined meta information.
        For example:
            nodeA
                nodeB
                    nodeC
        Here, combined_document_meta is the combined _meta_ information of node A, B and C.
        (this meta info can be found with _collect_entity_meta_by_path() util function).-
        """
        if not node.entity:
            return {}
        # If not passed a custom repository to save into, use the DocumentService's storage
        if not repository:
            repository: DataSource = self.repository_provider(data_source_id, self.user)  # type: ignore

        # If the node is a package, we build the path string to be used by filesystem like repositories.
        # Also, check for duplicate names in the package.
        if node.type == SIMOS.PACKAGE.value:
            path = f"{path}/{node.name}/" if path else f"{node.name}"
            if len(node.children) > 0:
                packageContent = node.children[0]
                contentListNames = []
                for child in packageContent.children:
                    if "name" in child.entity and child.name in contentListNames:
                        raise BadRequestException(
                            f"The document '{data_source_id}/{node.name}/{child.name}' already exists"
                        )
                    contentListNames.append(child.name)

        if update_uncontained:  # If flag is set, dig down and save uncontained documents
            for child in node.children:
                if child.is_array():
                    [
                        self.save(x, data_source_id, repository, path, update_uncontained, combined_document_meta)
                        for x in child.children
                    ]
                else:
                    self.save(child, data_source_id, repository, path, update_uncontained, combined_document_meta)

        if node.type == SIMOS.BLOB.value:
            node.entity = self.save_blob_data(node, repository)

        ref_dict = tree_node_to_ref_dict(node)

        if type(node) is Node:
            entity_has_all_required_attributes(ref_dict, node.blueprint.get_required_attributes())

        # If the node is not contained, and has data, save it!
        if not node.storage_contained and ref_dict:
            # To ensure the node has a _id
            if node.uid is None:
                raise ApplicationException(f"The document with name `{node.name}` is missing uid")

            # Expand this when adding new repositories requiring PATH
            if isinstance(repository, ZipFileClient):
                ref_dict["__path__"] = path
                ref_dict["__combined_document_meta__"] = combined_document_meta
            parent_uid = node.parent.node_id if node.parent else None
            repository.update(
                ref_dict,
                node.get_context_storage_attribute(),
                parent_id=parent_uid,
            )
            return {"_id": node.uid, "type": node.entity["type"], "name": node.name}
        return ref_dict

    def get_document_by_uid(
        self,
        data_source_id: str,
        document_uid: str,
        depth: int = 999,
    ) -> dict:
        return get_complete_sys_document(document_uid, self.repository_provider(data_source_id, self.user), depth)

    def get_node_by_uid(self, data_source_id: str, document_uid: str, depth: int = 999) -> Node:
        complete_document = get_complete_sys_document(
            document_uid, self.repository_provider(data_source_id, self.user), depth
        )
        return tree_node_from_dict(
            complete_document,
            uid=complete_document.get("_id"),
            blueprint_provider=self.get_blueprint,
            recipe_provider=self.get_storage_recipes,
        )

    def get_by_path(self, absolute_reference: str) -> Node:
        data_source_id, path, attribute = split_dmss_ref(absolute_reference)
        document_repository = get_data_source(data_source_id, self.user)
        document_id = get_document_uid_by_path(path, document_repository)
        return self.get_node_by_uid(data_source_id, document_id)

    def remove_document(self, data_source_id: str, document_id: str, attribute: str = None):
        """
        Delete a document, and any model contained children.
        If document_id is a dotted attribute path, it will remove the reference in the parent.
        Does not use the Node class, as blueprints won't necessarily be available when deleting.
        """
        repository = self.repository_provider(data_source_id, self.user)
        if attribute:
            root_document: dict = repository.get(document_id)
            path_after_root = attribute.split(".")
            nested_doc = root_document
            for index, attr in enumerate(path_after_root):
                if index + 1 == len(path_after_root):
                    if isinstance(nested_doc, list):
                        attr = int(attr)
                    potential_reference = nested_doc.pop(attr)
                    if potential_reference.get("_id") and potential_reference.get("contained") is True:
                        delete_document(repository, potential_reference["_id"])
                    break
                if isinstance(nested_doc, list):
                    nested_doc = nested_doc[int(attr)]
                else:
                    nested_doc = nested_doc[attr]
            repository.update(root_document)
            return
        else:
            delete_document(repository, document_id)

    def rename_document(self, data_source_id: str, document_id: str, name: str, parent_uid: str = None):
        # Only root-packages have no parent_id
        if not parent_uid:
            root_node: Node = self.get_node_by_uid(data_source_id, document_id)
            target_node = root_node

        # Grab the parent, and set target based on dotted document_id
        else:
            root_node: Node = self.get_node_by_uid(data_source_id, parent_uid)  # type: ignore
            target_node = root_node.search(document_id)

            if not target_node:
                raise NotFoundException(
                    message=f"Document with id '{document_id}' in data source '{data_source_id}' could not be found"
                )

        target_node.entity["name"] = name
        self.save(root_node, data_source_id)

        logger.info(f"Rename document '{target_node.node_id}' to '{name}")

        return {"uid": target_node.node_id}

    def update_document(
        self,
        data_source_id: str,
        document_id: str,
        data: Union[dict, list],
        attribute: str | None = None,
        files: dict = None,
        update_uncontained: bool = True,
    ):
        # TODO: Since we are only fetching 1 lvl here, any updates on nested uncontained attributes by dott reference
        # TODO: will fail, as they are not a node on the root node. For example; '123-456.contAttr.someUncontainedAttr'
        # TODO: We should update 'node.get_by_path()' do fetch documents as needed
        root: Node = self.get_node_by_uid(data_source_id, document_id, depth=0)
        target_node = root

        # If it's a contained nested node, set the modify target based on dotted-path
        if attribute:
            target_node = root.get_by_path(attribute.split("."))

        if not target_node:
            raise NotFoundException(f"{data_source_id}/{document_id}.{attribute}")

        target_node.update(data)
        if files:
            self._merge_entity_and_files(target_node, files)

        self.save(target_node, data_source_id, update_uncontained=update_uncontained)

        # If the target was a contained child of root, update root as well with any contained attributes
        if attribute and target_node.storage_contained:
            self.save(root, data_source_id, update_uncontained=False)

        logger.info(f"Updated document '{target_node.node_id}''")
        return {"data": tree_node_to_dict(target_node)}

    def add_document(self, absolute_ref: str, data: dict, update_uncontained: bool = False):
        data_source, parent_id, attribute = split_dmss_ref(absolute_ref)
        if parent_id and not attribute:
            raise BadRequestException("Attribute not specified on parent")
        if not data.get("type"):
            raise BadRequestException("Every entity must have a 'type' attribute")

        if not parent_id:  # No parent_id in reference. Just add the document to the root of the data_source
            return self._add_document_with_no_parent(data_source, data, update_uncontained)

        type = data["type"]
        parent_attribute = attribute.split(".")[0:-1]
        leaf_attribute = attribute.split(".")[-1]

        root: Node = self.get_node_by_uid(data_source, parent_id)
        if not root:
            raise NotFoundException(uid=parent_id)
        parent: Node = root.get_by_path(parent_attribute)

        leaf_parent = parent.get_by_path([leaf_attribute])
        if not leaf_parent:
            raise AttributeError(
                (
                    f"Invalid attribute given for type '{parent.type}'.\n"
                    + f"Valid attributes are {parent.blueprint.get_attribute_names()}.\n"
                    + f"Received '{leaf_attribute}'"
                )
            )

        # If the leaf attribute is a list. Set that as parent
        if leaf_parent.is_array():
            parent = leaf_parent
        entity: dict = data

        if type == SIMOS.BLUEPRINT.value and not entity.get("extends"):  # Extend default attributes and uiRecipes
            entity["extends"] = ["system/SIMOS/DefaultUiRecipes", "system/SIMOS/NamedEntity"]

        new_node_attribute = BlueprintAttribute(name=leaf_attribute, attribute_type=type)
        new_node = tree_node_from_dict(
            entity,
            blueprint_provider=self.get_blueprint,
            node_attribute=new_node_attribute,
            recipe_provider=self.get_storage_recipes,
        )

        required_attribute_names = [attribute.name for attribute in new_node.blueprint.get_required_attributes()]
        # If entity has a name, check if a file/attribute with the same name already exists on the target
        if "name" in required_attribute_names and parent.duplicate_attribute(new_node.name):
            raise BadRequestException(f"The document '{data_source}/{parent.name}/{new_node.name}' already exists")

        new_node.parent = parent
        new_node.set_uid()

        if isinstance(parent, ListNode):
            new_node.key = str(len(parent.children)) if parent.is_array() else new_node.attribute.name
            parent.add_child(new_node)
        else:
            parent.replace(new_node.node_id, new_node)

        new_node.validate_type_on_parent()

        self.save(root, data_source, update_uncontained=update_uncontained)

        return {"uid": new_node.node_id}

    def _add_document_with_no_parent(self, data_source: str, data: dict, update_uncontained: bool = False):
        if data.get("type") != SIMOS.PACKAGE.value and not data.get("isRoot"):
            raise BadRequestException("Only root packages may be added without a parent.")

        new_node = tree_node_from_dict(
            data, blueprint_provider=self.get_blueprint, recipe_provider=self.get_storage_recipes
        )

        exisiting_root_package = get_data_source(data_source, self.user).find(
            {"type": SIMOS.PACKAGE.value, "isRoot": True, "name": data["name"]}
        )
        if exisiting_root_package:
            raise BadRequestException(f"The document '{data_source}/{new_node.name}' already exists")

        new_node.set_uid()

        self.save(new_node, data_source, update_uncontained=update_uncontained)

        return {"uid": new_node.node_id}

    def remove_by_path(self, data_source_id: str, directory: str, attribute: str = None):
        if attribute:
            raise ApplicationException(
                "Removing a document by path in combination with attribute is not yet supported"
            )
        directory = directory.rstrip("/").lstrip("/")
        data_source = self.repository_provider(data_source_id, self.user)

        if "/" in directory:
            parent_uid = get_document_uid_by_path(f"{'/'.join(directory.split('/')[0:-1])}", data_source)
            child_uid = get_document_uid_by_path(directory, data_source)
            parent_node = self.get_node_by_uid(data_source_id, parent_uid)

            # find the node id of the child with uid equal to child_uid
            child_node_ids = (child.node_id for child in parent_node.children[0].children if child.uid == child_uid)
            child_node_id = next(child_node_ids)

            # The first child of a directory is always 'content'
            parent_node.children[0].remove_by_child_id(child_node_id)
            self.save(parent_node, data_source_id)
            delete_document(data_source, document_id=child_uid)
            return

        # We are removing a root-package with no parent
        document_id = get_document_uid_by_path(directory, data_source)
        delete_document(data_source, document_id)

    @staticmethod
    def _merge_entity_and_files(node: Node, files: Dict[str, BinaryIO]):
        """
        Recursively adds the matching posted files to the system/SIMOS/Blob types in the node
        """
        for node in node.traverse():  # Traverse the entire Node tree
            if not node.entity:  # Skipping empty nodes
                continue
            if node.type == SIMOS.BLOB.value:
                try:  # For all Blob Nodes, add the posted file in the Node temporary '_blob_' attribute
                    node.entity["_blob_"] = files[node.entity["name"]]
                except KeyError:
                    raise KeyError(
                        "File referenced in entity does not match any ",
                        f"filename posted. Posted files: {tuple(files.keys())}",
                    )

    def add(
        self,
        data_source_id: str,
        path: str | None,
        document: Entity,
        files: dict[str, BinaryIO],
        update_uncontained=False,
    ):
        """Add en entity to path
        path: dotted path on format 'RootPackage/folder/entity.attribute.attribute.
            If none, we're adding to the data source itself.
        document: The entity to be added
        files: Dict with names and files of the files contained in the document
        update_uncontained: Whether to update uncontained children
        """
        document_dict = document.dict()
        if not path:  # We're adding something to the dataSource itself
            if not document.type == SIMOS.PACKAGE.value or not document_dict.get("isRoot", False):
                raise BadRequestException("Only root packages may be added to the root of a data source")
            # TODO: Validate package entity
            try:
                if get_document_uid_by_path(
                    document_dict["name"], self.repository_provider(data_source_id, self.user)
                ):
                    raise ValidationException(
                        message=f"A root package named '{document_dict['name']}' already exists",
                        data={"dataSource": data_source_id, "document": document_dict},
                    )
            except NotFoundException:
                pass
            document_repository = self.repository_provider(data_source_id, self.user)
            document_repository.update(document_dict)
            return {"uid": document_dict["_id"]}

        target: Node = self.get_by_path(f"{data_source_id}/{path}")
        if not target:
            raise NotFoundException(f"Could not find '{path}' in data source '{data_source_id}'")

        # If dotted attribute path, attribute is the last entry. Else content
        new_node_attr = path.split(".")[-1] if "." in path else "content"

        new_node = tree_node_from_dict(
            {**document_dict},
            blueprint_provider=self.get_blueprint,
            node_attribute=BlueprintAttribute(name=new_node_attr, attribute_type=document.type),
            recipe_provider=self.get_storage_recipes,
        )
        new_node.set_uid()

        if files:
            self._merge_entity_and_files(new_node, files)

        self.save(new_node, data_source_id, update_uncontained=update_uncontained)

        if target.type == SIMOS.PACKAGE.value:
            target = target.children[0]  # Set target to be the packages content
        if isinstance(target, ListNode):
            new_node.parent = target
            target.add_child(new_node)
            self.save(target.parent, data_source_id, update_uncontained=False)
        else:
            new_node.parent = target.parent
            target = new_node
            self.save(target, data_source_id, update_uncontained=False)

        return {"uid": new_node.node_id}

    def search(self, data_source_id, search_data, dotted_attribute_path):
        repository: DataSource = self.repository_provider(data_source_id, self.user)

        if not isinstance(repository.get_default_repository().client, MongoDBClient):
            raise ApplicationException(
                f"Search is not supported on this repository type; {type(repository.repository).__name__}"
            )

        try:
            process_search_data = build_mongo_query(self.get_blueprint, search_data)
        except ValueError as error:
            logger.warning(f"Failed to build mongo query; {error}")
            raise BadRequestException("Failed to build mongo query")
        result: List[dict] = repository.find(process_search_data)
        result_sorted: List[dict] = sort_dtos_by_attribute(result, dotted_attribute_path)
        result_list = {}
        for document in result_sorted:
            result_list[f"{data_source_id}/{document['_id']}"] = document

        return result_list

    def set_acl(self, data_source_id: str, document_id: str, acl: ACL, recursively: bool = True):
        if "." in document_id:
            raise Exception(
                f"set_acl() function got document_id: {document_id}. "
                f"The set_acl() function can only be used on root documents. You cannot use a dotted document id."
            )
        data_source: DataSource = self.repository_provider(data_source_id, self.user)

        if not recursively:  # Only update acl on the one document
            data_source.update_access_control(document_id, acl)
            return

        root_node = self.get_node_by_uid(data_source_id, document_id)
        data_source.update_access_control(root_node.node_id, acl)
        for child in root_node.children:
            for node in child.traverse():
                if not node.storage_contained and not node.is_array():
                    try:
                        data_source.update_access_control(node.entity["_id"], acl)
                    except MissingPrivilegeException:  # The user might not have permission on a referenced document
                        logger.warning(f"Failed to update ACL on {node.node_id}. Permission denied.")

    def get_acl(self, data_source_id, document_id) -> ACL:
        data_source: DataSource = self.repository_provider(data_source_id, self.user)
        lookup = data_source.get_access_control(document_id)
        return lookup.acl

    def insert_reference(
        self, data_source_id: str, document_id: str, reference: Reference, attribute_path: str
    ) -> dict:
        root: Node = self.get_node_by_uid(data_source_id, document_id)
        attribute_node: Node = root.search(f"{document_id}.{attribute_path}")
        if not attribute_node:
            raise NotFoundException(uid=document_id + attribute_path)

        # Check that target exists and has correct values
        # The SIMOS/Entity type can reference any type (used by Package)
        referenced_document: dict = self.repository_provider(data_source_id, self.user).get(reference.uid)
        if not referenced_document:
            raise NotFoundException(uid=f"{data_source_id}/{reference.uid}")
        if BuiltinDataTypes.OBJECT.value != attribute_node.type != referenced_document["type"]:
            raise BadRequestException(
                f"The referenced entity should be of type '{attribute_node.type}'"
                f", but was '{referenced_document['type']}'"
            )
        if reference.type != referenced_document["type"]:
            raise BadRequestException(
                f"The 'type' value of the reference does not match the referenced document."
                f"{reference.type} --> {referenced_document['type']}"
            )
        # If the node to update is a list, append to end
        if attribute_node.is_array():
            attribute_node.add_child(
                tree_node_from_dict(
                    entity={**reference.dict(by_alias=True), "_id": str(reference.uid)},
                    uid=str(reference.uid),
                    blueprint_provider=self.get_blueprint,
                    recipe_provider=self.get_storage_recipes,
                    node_attribute=attribute_node.attribute,
                )
            )
        else:
            attribute_node.entity = {**reference.dict(by_alias=True), "_id": str(reference.uid)}
            attribute_node.uid = str(reference.uid)
            attribute_node.type = reference.type

        self.save(root, data_source_id, update_uncontained=False)

        logger.info(
            f"Inserted reference to '{referenced_document['_id']}'"
            f" as '{attribute_path}' in '{root.name}'({root.uid})"
        )

        return tree_node_to_dict(root)

    def remove_reference(self, data_source_id: str, document_id: str, attribute_path: str) -> dict:
        root: Node = self.get_node_by_uid(data_source_id, document_id)
        attribute_node = root.get_by_path(attribute_path.split("."))
        if not attribute_node:
            raise Exception(f"Could not find the '{attribute_path}' Node on '{document_id}'")

        # If we are removing a reference from a list, pop child with posted index
        if attribute_node.parent.is_array():
            attribute_node.parent.children.pop(int(attribute_path.split(".")[-1]))
        else:
            attribute_node.entity = {}
        self.save(root, data_source_id)
        logger.info(f"Removed reference for '{attribute_path}' in '{root.name}'({root.uid})")

        return tree_node_to_dict(root)
