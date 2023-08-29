import mimetypes
import pprint
from functools import lru_cache
from typing import Callable, Dict, List, Union
from uuid import uuid4

from common.address import Address
from common.exceptions import (
    ApplicationException,
    BadRequestException,
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
from common.utils.get_storage_recipe import (
    create_default_storage_recipe,
    storage_recipe_provider,
)
from common.utils.logging import logger
from common.utils.resolve_address import ResolvedAddress, resolve_address
from common.utils.sort_entities_by_attribute import sort_dtos_by_attribute
from common.utils.validators import validate_entity_against_self
from config import config, default_user
from domain_classes.blueprint import Blueprint
from domain_classes.storage_recipe import StorageRecipe
from domain_classes.tree_node import ListNode, Node
from enums import REFERENCE_TYPES, SIMOS
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

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def get_storage_recipes(self, type: str, context: str | None = None) -> list[StorageRecipe]:
        if not context:
            return create_default_storage_recipe()

        # TODO: Support other contexts
        if context_recipes := self._recipe_provider(type, context=context):
            return context_recipes

        # No storage recipes created for contex. Creating defaults
        return create_default_storage_recipe()

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

        if isinstance(node, Node) and node.should_have_id():
            node.set_uid(node.generate_id())  # Ensure the node has a _id
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
    def get_document(self, address: Address, depth: int = 0) -> Node | ListNode:
        """
        Get document by address.

        :param address: Address to the entity you wish to obtain
        :param depth:
            depth is used to control if references (storage and link) should be resolved (it does not affect contained attributes)
              depth=0 means that if the address is pointing to a reference it will be returned directly without being resolved first.
              depth=1 means that if the address is pointing to a reference it will be resolved before returned. Child references will not be resolved.
              depth=2 means that the entity's direct child references will be returned as well.
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
                depth_count=1,
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

    def remove(self, address: Address) -> None:
        node = self.get_document(address)
        if node.parent and not node.attribute.is_optional:
            raise ValidationException("Tried to remove a required attribute")

        data_source = self.repository_provider(address.data_source, self.user)
        resolved_reference: ResolvedAddress = resolve_address(address, self.get_data_source)
        # If the reference goes through a parent, get the parent document
        if resolved_reference.attribute_path:
            document = data_source.get(resolved_reference.document_id)
            new_document = delete_by_attribute_path(document, resolved_reference.attribute_path, data_source)
            data_source.update(new_document)
            return

        delete_document(data_source, resolved_reference.document_id)

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
