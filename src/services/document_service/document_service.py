import mimetypes
import pprint
from collections.abc import Callable
from uuid import uuid4

from authentication.models import User
from common.address import Address
from common.entity.is_reference import is_reference
from common.entity.validators import validate_entity_against_self
from common.exceptions import (
    ApplicationException,
    BadRequestException,
    NotFoundException,
    ValidationException,
)
from common.providers.address_resolver.address_resolver import (
    ResolvedAddress,
    resolve_address,
)
from common.providers.address_resolver.reference_resolver import resolve_references_in_entity
from common.providers.blueprint_provider import get_blueprint_provider
from common.providers.storage_recipe_provider import (
    create_default_storage_recipe,
    storage_recipe_provider,
)
from common.tree.tree_node import ListNode, Node
from common.tree.tree_node_serializer import (
    tree_node_from_dict,
    tree_node_to_dict,
    tree_node_to_ref_dict,
)
from common.utils.logging import logger
from common.utils.update_nested_dict import update_nested_dict
from domain_classes.blueprint import Blueprint
from domain_classes.storage_recipe import StorageRecipe
from enums import REFERENCE_TYPES, SIMOS
from services.document_service.delete_documents import (
    delete_by_attribute_path,
    delete_document,
)
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source
from storage.repositories.zip.zip_file_client import ZipFileClient

pretty_printer = pprint.PrettyPrinter()


class DocumentService:
    def __init__(
        self,
        repository_provider=get_data_source,
        blueprint_provider=None,
        user=User.default(),
        context: str | None = None,
        recipe_provider=None,
    ):
        self._blueprint_provider = blueprint_provider or get_blueprint_provider()
        self._recipe_provider: Callable[..., list[StorageRecipe]] = recipe_provider or storage_recipe_provider
        self.repository_provider = repository_provider
        self.user = user
        self.context = context
        self.get_data_source = lambda data_source_id: self.repository_provider(data_source_id, self.user)

    def get_blueprint(self, type: str) -> Blueprint:
        return self._blueprint_provider.get_blueprint_with_extended_attributes(type)

    def get_storage_recipes(self, type: str, context: str | None = None) -> list[StorageRecipe]:
        if not context:
            return create_default_storage_recipe()

        # TODO: Support other contexts
        if context_recipes := self._recipe_provider(type, context=context):
            return context_recipes

        # No storage recipes created for contex. Creating defaults
        return create_default_storage_recipe()

    def invalidate_cache(self):
        pass

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
        node: Node | ListNode,
        data_source_id: str,
        repository=None,
        path="",
        combined_document_meta: dict | None = None,
        initial: bool = False,
    ) -> dict:
        """
        Saves a Node.
        Converting uncontained child entities to references.

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
                node.parent,
                data_source_id,
                repository,
                path,
                combined_document_meta,
                initial,
            )
        if not node.entity:
            return {}
        # If not passed a custom repository to save into, use the DocumentService's storage
        if not repository:
            repository: DataSource = self.repository_provider(data_source_id, self.user)  # type: ignore

        # If the node is a package, we build the path string to be used by filesystem like repositories.
        # Also, check for duplicate names in the package.
        if node.type == SIMOS.PACKAGE.value:
            self.raise_for_duplicate_name(node, data_source_id)

        for child in node.children:
            if child.is_array():
                [
                    self.save(x, data_source_id, repository, path, combined_document_meta)
                    for x in child.children
                    if x.type != SIMOS.REFERENCE.value
                ]
            elif child.type != SIMOS.REFERENCE.value:
                self.save(child, data_source_id, repository, path, combined_document_meta)
        if node.type == SIMOS.BLOB.value:
            node.entity = self.save_blob_data(node, repository)

        if isinstance(node, Node) and node.should_have_id():
            node.set_uid(node.generate_id())  # Ensure the node has a _id
        ref_dict = tree_node_to_ref_dict(node)

        # If the node is not contained, and has data, save it!
        if not node.storage_contained and node.contained:
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

    def resolve_document(self, address: Address, depth: int = 0) -> tuple[dict, ResolvedAddress]:
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

            if address.is_by_package():
                # If the address is by package (package/sub-package/entity),
                # then the entity in the resolved address will be a reference to the entity.
                # This reference needs to be resolved before continue, since by package means (by definition),
                # that the entity should be resolved.
                resolved_address = resolve_address(
                    Address.from_relative(
                        resolved_address.entity["address"],
                        resolved_address.document_id,
                        resolved_address.data_source_id,
                    ),
                    self.get_data_source,
                )

            if depth == 0:
                # return without any resolving
                return resolved_address.entity, resolved_address

            while is_reference(resolved_address.entity):
                # if the address is pointing to a reference (or chain of references) resolve those
                resolved_address = resolve_address(
                    Address.from_relative(
                        resolved_address.entity["address"],
                        resolved_address.document_id,
                        resolved_address.data_source_id,
                        resolved_address.attribute_path,
                    ),
                    self.get_data_source,
                )

            # start resolving any references if depth > 1
            resolved_document: dict = resolve_references_in_entity(
                resolved_address.entity,
                self.get_data_source(resolved_address.data_source_id),
                self.get_data_source,
                resolved_address.document_id,
                depth=depth,
                depth_count=1,
                path=resolved_address.attribute_path,
            )
            return resolved_document, resolved_address
        except (NotFoundException, ApplicationException) as e:
            e.data = e.dict()
            e.debug = e.message
            e.message = f"Failed to get document referenced with '{address}'"
            raise e

    def get_document(self, address: Address, depth: int = 0) -> Node | ListNode:
        resolved_document, resolved_address = self.resolve_document(address, depth)

        if len(resolved_address.attribute_path) > 0:
            # We need to get the whole (root) document before continue,
            # this is because the returned node is used when saving,
            # and it assumes that the node contains the whole document.
            data_source: DataSource = self.get_data_source(resolved_address.data_source_id)
            document: dict = data_source.get(resolved_address.document_id)
            nested_path_to_update: list[str] = [x.strip("[]") for x in resolved_address.attribute_path]
            update_nested_dict(document, nested_path_to_update, resolved_document)
            resolved_document = document

        node: Node = tree_node_from_dict(
            resolved_document,
            uid=resolved_address.document_id,
            blueprint_provider=self.get_blueprint,
            recipe_provider=self.get_storage_recipes,
            data_source=resolved_address.data_source_id,
        )

        if resolved_address.attribute_path:
            child = node.get_by_path(resolved_address.attribute_path)
            if not child:
                raise NotFoundException(f"Invalid path {resolved_address.attribute_path}")
            return child
        return node

    def remove(self, address: Address) -> None:
        node = self.get_document(address)
        if node.parent and not node.is_optional:
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

    def raise_for_duplicate_name(self, node, data_source_id):
        if len(node.children) > 0:
            contentListNames = []
            for child in node.children[0].children:
                if child.type == SIMOS.REFERENCE.value:
                    try:
                        entity = self.get_document(Address(child.entity["address"], data_source_id), depth=0).entity
                    except NotFoundException:
                        """
                        reference does not point to anything because the document it points to has not been uploaded
                        yet. dm-cli was probably used
                        """
                        logger.debug("A reference that does not point to anything was received.")
                        continue
                else:
                    entity = child.entity
                if item_name := entity.get("name"):
                    # Content of a package should not have duplicate name, but name is not required for all document
                    if item_name in contentListNames:
                        raise BadRequestException(
                            f"The document '{data_source_id}/{node.entity['name']}/{child.entity['name']}' already exists"
                        )

                    contentListNames.append(item_name)
