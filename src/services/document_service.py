import mimetypes
import pprint
from functools import lru_cache
from typing import BinaryIO, Callable, Dict, List, Union
from uuid import uuid4

from authentication.models import ACL
from common.address import Address
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
from common.utils.delete_documents import delete_by_attribute_path, delete_document
from common.utils.get_blueprint import get_blueprint_provider
from common.utils.get_resolved_document_by_id import resolve_references_in_entity
from common.utils.get_storage_recipe import storage_recipe_provider
from common.utils.logging import logger
from common.utils.resolve_address import ResolvedAddress, resolve_address, split_path
from common.utils.sort_entities_by_attribute import sort_dtos_by_attribute
from common.utils.validators import validate_entity, validate_entity_against_self
from config import config, default_user
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS, BuiltinDataTypes, StorageDataTypes
from restful.request_types.shared import Entity
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
        self.get_data_source = lambda data_source_id: self.repository_provider(data_source_id, self.user)

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

    def save_blob_data(self, node: Node, repository: DataSource) -> dict:
        """
        Updates the posted blob and unlink the binary file from the Node.
        Returns a system/SIMOS/Blob entity with the created id.

        This function assumes that the parameter 'node' has an entity of type system/SIMOS/Blob,
        and assumes that system/SIMOS/Blob blueprint has name as a required attribute.
        """
        if node.entity["type"] != SIMOS.BLOB.value:
            raise ApplicationException(f"Cannot save blob data for types other than {SIMOS.BLOB.value}")
        if file := node.entity.get("_blob_"):  # If a file was posted with the same name as this blob, save it
            # Get or set the "_blob_id"
            node.entity["_blob_id"] = node.entity["_blob_id"] if node.entity.get("_blob_id") else str(uuid4())
            # Save it
            content_type = mimetypes.guess_type(node.entity.get("name"))
            repository.update_blob(node.entity["_blob_id"], node.entity.get("name"), content_type, file)
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
        initial: bool = False,
    ) -> Dict:
        """
        Recursively saves a Node.
        Digs down to the leaf children, and based on storageContained,
        either saves the entity and returns the Reference, OR returns the entire entity.

        node: The Node to save
        path: A Filesystem equivalent path for this node. Used when writing zip-files.
        combined_document_meta:  The combined meta information.
            For example:
                nodeA
                    nodeB
                        nodeC
            Here, combined_document_meta is the combined _meta_ information of node A, B and C.
            (this meta info can be found with _collect_entity_meta_by_path() util function).-
        initial:  When true, the function will move up the tree until it finds a storage non-contained node, and start saving from there.
            This allows us to call "save()" on any node, without having to find the "root node" (storage non-contained)

        """
        if initial and node.storage_contained:
            self.save(
                node.parent, data_source_id, repository, path, update_uncontained, combined_document_meta, initial
            )
        if not node.entity:
            return {}
        # If not passed a custom repository to save into, use the DocumentService's storage
        if not repository:
            repository: DataSource = self.repository_provider(data_source_id, self.user)  # type: ignore

        # If the node is a package, we build the path string to be used by filesystem like repositories.
        # Also, check for duplicate names in the package.
        if node.type == SIMOS.PACKAGE.value:
            path = f"{path}/{node.entity['name']}/" if path else f"{node.entity['name']}"
            if len(node.children) > 0:
                packageContent = node.children[0]
                contentListNames = []
                for child in packageContent.children:
                    if "name" in child.entity:
                        # Content of a package should not have duplicate name, but name is not required for all document
                        if child.entity["name"] in contentListNames:
                            raise BadRequestException(
                                f"The document '{data_source_id}/{node.entity['name']}/{child.entity['name']}' already exists"
                            )

                        contentListNames.append(child.entity["name"])

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

        node.set_uid()  # Ensure the node has a _id
        ref_dict = tree_node_to_ref_dict(node)

        # If the node is not contained, and has data, save it!
        if not node.storage_contained and ref_dict and node.uid is not None:
            # Expand this when adding new repositories requiring PATH
            if isinstance(repository, ZipFileClient):
                ref_dict["__path__"] = path
                ref_dict["__combined_document_meta__"] = combined_document_meta
            parent_uid = node.parent.node_id if node.parent else None
            validate_entity_against_self(tree_node_to_dict(node), self.get_blueprint)
            repository.update(
                ref_dict,
                node.get_context_storage_attribute(),
                parent_id=parent_uid,
            )
            result = {
                "type": SIMOS.REFERENCE.value,
                "address": f"${node.uid}",
                "referenceType": REFERENCE_TYPES.STORAGE.value,
            }
            return result
        return ref_dict

    # TODO: Dont return Node. Doing this is ~33% slower
    def get_document(self, address: Address, depth: int = 0, resolve_references: bool = False) -> Node | ListNode:
        """
        Get document by address.

        :param address: Address to the entity you wish to obtain
        :param depth: depth=0 means that the entire entity will be returned, except any references it may contain
            along the tree. depth=1 means that the entity's direct child references will be returned as well.
        :param resolve_references: If false, references will not be resolved, no
            matter the depth. If true, they will be resolved if the depth param allows it
        """
        try:
            resolved_address: ResolvedAddress = resolve_address(address, self.get_data_source)
            data_source: DataSource = self.get_data_source(resolved_address.data_source_id)
            document: dict = data_source.get(resolved_address.document_id)

            resolved_document: dict = resolve_references_in_entity(
                document,
                data_source,
                self.get_data_source,
                resolved_address.document_id,
                depth=depth + len(list(filter(lambda x: x[0] != "[", resolved_address.attribute_path))),
                depth_count=0,
                resolve_references=resolve_references,
            )

            node: Node = tree_node_from_dict(
                resolved_document,
                uid=resolved_address.document_id,
                blueprint_provider=self.get_blueprint,
                recipe_provider=self.get_storage_recipes,
            )

            if resolved_address.attribute_path:
                child = node.get_by_path(resolved_address.attribute_path)
                if not child:
                    raise NotFoundException(f"Invalid path {resolved_address.attribute_path}")
                return child
            return node
        except (NotFoundException, ApplicationException) as e:
            e.debug = f"{e.message}. {e.debug}"
            e.message = f"Failed to get document referenced with '{address}'"
            raise e

    def _get_node_to_update(self, address: Address, node_entity: Union[dict, list]) -> Union[Node, ListNode]:
        """
        Updating a document is done by fetching the node. This functions returns a node specified by reference.
        Note: if the node specified by reference does not exist, it will be created if and only if the attribute is
        specified as optional in the blueprint.
        """
        path_parts = split_path(address.path)
        parent_path = "".join(path_parts[:-1])
        parent_node: Node = self.get_document(Address(parent_path, address.data_source), depth=0)
        parent_blueprint_attribute_names = [attribute.name for attribute in parent_node.blueprint.attributes]
        attribute_to_update = path_parts[-1].strip(".").strip("[]")
        node = parent_node.get_by_ref_part([attribute_to_update])

        attribute_to_update_does_not_exist_in_parent_document = node is None

        if (
            attribute_to_update_does_not_exist_in_parent_document
            and attribute_to_update in parent_blueprint_attribute_names
        ):
            attribute = [
                attribute for attribute in parent_node.blueprint.attributes if attribute.name == attribute_to_update
            ][0]

            # We only want to add the attribute if it does not already exist AND is optional.
            if not attribute.is_optional:
                raise ValidationException(f"Could not update node. attribute '{attribute.name}' is not optional.")
            if attribute.is_array:
                node = ListNode(
                    key=attribute_to_update,
                    attribute=attribute,
                    blueprint_provider=self.get_blueprint,
                    entity=node_entity,
                )
            else:
                node = Node(
                    key=attribute_to_update,
                    entity=node_entity,
                    attribute=attribute,
                    blueprint_provider=self.get_blueprint,
                )
        elif (
            attribute_to_update_does_not_exist_in_parent_document
            and attribute_to_update not in parent_blueprint_attribute_names
        ):
            raise ApplicationException(
                f"Could not get node to update. Attribute {attribute_to_update} was not found in the list of attributes on the parents blueprint ({parent_blueprint_attribute_names})."
            )
        node.parent = parent_node
        return node

    def update_document(
        self,
        address: Address,
        data: Union[dict, list],
        files: dict = None,
        update_uncontained: bool = True,  # TODO: Remove this flag
    ):
        """
        Update a document.

        What to update is referred to with an address.
        It can either be an entire document or just an attribute inside a document.
        """
        validate_entity_against_self(data, self.get_blueprint)
        if not address.path:
            raise Exception(f"Could not find the node on '{address}'")
        path_parts = split_path(address.path)

        # Since the node targeted by the reference might not exist (e.g. optional complex attribute)
        # we aim for the parent node first. Then get the child.
        if len(path_parts) > 1:
            node: Union[Node, ListNode] = self._get_node_to_update(address=address, node_entity=data)
        else:
            node: Node = self.get_document(address)  # type: ignore

        if node.attribute.attribute_type != BuiltinDataTypes.OBJECT.value:
            validate_entity(data, self.get_blueprint, self.get_blueprint(node.attribute.attribute_type), "extend")
            # TODO consider validating link reference objects if the data parameter is of type system/SIMOS/Reference.

        node.update(data)
        if files:
            self._merge_entity_and_files(node, files)

        self.save(node, address.data_source, update_uncontained=update_uncontained, initial=True)
        if len(path_parts) > 1:
            node.parent.children.append(node)
            self.save(node.parent, address.data_source, update_uncontained=update_uncontained, initial=True)
        logger.info(f"Updated entity '{address}'")
        return {"data": tree_node_to_dict(node)}

    def remove(self, address: Address) -> None:
        data_source = self.repository_provider(address.data_source, self.user)

        resolved_reference: ResolvedAddress = resolve_address(address, self.get_data_source)
        # If the reference goes through a parent, get the parent document
        if resolved_reference.attribute_path:
            document = data_source.get(resolved_reference.document_id)
            new_document = delete_by_attribute_path(document, resolved_reference.attribute_path, data_source)
            data_source.update(new_document)
            return

        delete_document(data_source, resolved_reference.document_id)

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

    def _add_document_to_data_source(self, data_source_id: str, document: dict, update_uncontained: bool = False):
        if document.get("type") != SIMOS.PACKAGE.value and not document.get("isRoot"):
            raise BadRequestException("Only root packages may be added without a parent.")

        new_node = tree_node_from_dict(
            document, blueprint_provider=self.get_blueprint, recipe_provider=self.get_storage_recipes
        )

        try:
            if self.get_document(Address(new_node.entity["name"], data_source_id), resolve_references=True, depth=99):
                raise ValidationException(
                    message=f"A root package named '{new_node.entity['name']}' already exists",
                    data={"dataSource": data_source_id, "document": document},
                )
        except NotFoundException:
            pass

        new_node.set_uid()

        self.save(new_node, data_source_id, update_uncontained=update_uncontained)

        return {"uid": new_node.node_id}

    def add(
        self,
        address: Address,
        document: dict,
        files: dict[str, BinaryIO] | None = None,
        update_uncontained=False,
    ):
        """Add en entity to path
        reference: reference to a package or a data source.
        document: The entity to be added
        files: Dict with names and files of the files contained in the document
        update_uncontained: Whether to update uncontained children
        """
        validate_entity_against_self(document, self.get_blueprint)
        entity: Entity = Entity(**document)

        if not address.path:  # We're adding something to the dataSource itself
            return self._add_document_to_data_source(address.data_source, document, update_uncontained)

        target: Node = self.get_document(address, resolve_references=True, depth=99)

        if not target:
            raise NotFoundException(f"Could not find '{address}' in data source '{address.data_source}'")

        if target.type != SIMOS.PACKAGE.value and target.type != "object":
            validate_entity(
                document, self.get_blueprint, self.get_blueprint(target.attribute.attribute_type), "extend"
            )

        new_node = tree_node_from_dict(
            {**document},
            blueprint_provider=self.get_blueprint,
            node_attribute=BlueprintAttribute(name=target.attribute.name, attribute_type=entity.type),
            recipe_provider=self.get_storage_recipes,
        )

        if not target.is_array() and target.type != SIMOS.PACKAGE.value:
            required_attribute_names = [attribute.name for attribute in new_node.blueprint.get_required_attributes()]
            # If entity has a name, check if a file/attribute with the same name already exists on the target
            if "name" in required_attribute_names and target.parent.duplicate_attribute(
                new_node.entity.get("name", new_node.attribute.name)
            ):
                raise BadRequestException(
                    f"The document at '{address}' already has a child with name '{new_node.entity.get('name', new_node.attribute.name)}'"
                )

        if files:
            self._merge_entity_and_files(new_node, files)

        if target.type == SIMOS.PACKAGE.value:
            target = target.children[0]  # Set target to be the packages content

        if isinstance(target, ListNode) or target.parent.type == SIMOS.PACKAGE.value:
            new_node.set_uid()
            new_node.parent = target
            new_node.key = str(len(target.children))
            target.add_child(new_node)
            self.save(target.find_parent(), address.data_source, update_uncontained=False)
        else:
            new_node.parent = target.parent
            target.parent.replace(new_node.node_id, new_node)
            self.save(target.find_parent(), address.data_source, update_uncontained=False)

        self.save(new_node, address.data_source, update_uncontained=update_uncontained)

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

        # TODO: Updating ACL for Links should only be additive
        # TODO: ACL for StorageReferences should always be identical to parent document
        root_node = self.get_document(Address(document_id, data_source_id), 99, resolve_references=True)
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
        if document_id.startswith("$"):
            document_id = document_id[1:]
        lookup = data_source.get_access_control(document_id)
        return lookup.acl

    def remove_reference(self, address: Address) -> dict:
        attribute_node: Node = self.get_document(address)
        if not address.path:
            raise Exception(f"Could not find the node on '{address}'")
        document: Node = attribute_node.parent.find_parent()

        # If we are removing a reference from a list, pop child with posted index
        if attribute_node.parent.is_array():
            attribute_node.parent.children.pop(int(attribute_node.key))
        else:
            attribute_node.entity = {}
        self.save(document, address.data_source)
        logger.info(f"Removed reference from '{address}'")

        return tree_node_to_dict(document)
