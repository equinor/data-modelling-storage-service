import pprint
import zipfile
from functools import lru_cache
from tempfile import SpooledTemporaryFile
from typing import Callable, Dict, List, Union
from uuid import uuid4

from config import Config
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.dto import DTO
from domain_classes.storage_recipe import StorageRecipe
from domain_classes.tree_node import ListNode, Node
from enums import BLOB_TYPES, DMT, SIMOS
from restful.request_types.shared import NamedEntity, Reference
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source
from storage.repositories.mongo import MongoDBClient
from storage.repositories.zip import ZipFileClient
from utils.build_complex_search import build_mongo_query
from utils.create_entity import CreateEntity
from utils.exceptions import (
    DuplicateFileNameException,
    EntityNotFoundException,
    FileNotFoundException,
    InvalidDocumentNameException,
    InvalidEntityException,
    RepositoryException,
)
from utils.get_blueprint import BlueprintProvider
from utils.logging import logger
from utils.string_helpers import url_safe_name
from utils.validators import valid_named_entity

pretty_printer = pprint.PrettyPrinter()


def get_resolved_document(
    document: DTO,
    document_repository: DataSource,
    blueprint_provider: Callable[[str], Blueprint],
    depth: int = 999,
    depth_count: int = 0,
) -> Dict:
    if depth <= depth_count:
        if depth_count >= 999:
            raise RecursionError("Reached max-nested-depth (999). Most likely some recursive entities")
        return document.data
    depth_count += 1

    blueprint: Blueprint = blueprint_provider(document.type)

    data: Dict = document.data

    for complex_attribute in blueprint.get_none_primitive_types():
        attribute_name = complex_attribute.name
        if complex_data := document.get(attribute_name):
            storage_recipe: StorageRecipe = blueprint.storage_recipes[0]
            if storage_recipe.is_contained(attribute_name, complex_attribute.attribute_type):
                if complex_attribute.is_array():
                    temp = []
                    for item in complex_data:
                        # Only optional, and unfixed array attributes are allowed to have empty{} items.
                        if not item and (complex_attribute.is_optional() or complex_attribute.dimensions.is_unfixed()):
                            temp.append({})
                        else:
                            try:
                                temp.append(
                                    get_resolved_document(
                                        DTO(item), document_repository, blueprint_provider, depth, depth_count
                                    )
                                )
                            except Exception as error:
                                # error = f"The entity {item} is invalid! Type: {complex_attribute.attribute_type}"
                                logger.exception(error)
                                raise Exception(error)

                    document.data[attribute_name] = temp
                else:
                    data[attribute_name] = get_resolved_document(
                        DTO(complex_data), document_repository, blueprint_provider, depth, depth_count
                    )
            else:
                if complex_attribute.is_array():
                    children = []
                    for item in complex_data:
                        try:
                            valid_named_entity(item)
                            doc = get_complete_document(item["_id"], document_repository, blueprint_provider, depth)
                        except InvalidEntityException as error:
                            raise InvalidEntityException(
                                f"{pprint.pformat(data)} is invalid.\n message: {error}"
                            ) from None
                        except EntityNotFoundException as error:
                            raise InvalidEntityException(
                                f"The document {{'name': {document.name}, '_id': {document.uid}}} has in invalid "
                                f"child, and could not be loaded. Error: {error.message}"
                            ) from None
                        children.append(doc)
                    data[attribute_name] = children
                else:
                    try:
                        valid_named_entity(complex_data)
                    except InvalidEntityException as error:
                        raise InvalidEntityException(
                            f"{pprint.pformat(data)} is invalid.\n message: {error}"
                        ) from None
                    data[attribute_name] = get_complete_document(
                        complex_data["_id"], document_repository, blueprint_provider, depth
                    )
        # If there is no data, and the attribute is NOT optional, AND it's NOT an array, raise an exception
        else:
            if not complex_attribute.is_optional() and not complex_attribute.is_array():
                error = f"The entity {document.name} is invalid! None-optional type '{attribute_name}' is missing."
                logger.error(error)

    return data


def get_complete_document(
    document_uid: str,
    document_repository: DataSource,
    blueprint_provider: Callable[[str], Blueprint],
    depth: int = 999,
) -> dict:
    raw_document = document_repository.get(str(document_uid))
    return get_resolved_document(raw_document, document_repository, blueprint_provider, depth)


class DocumentService:
    def __init__(self, repository_provider=get_data_source, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider
        self.repository_provider = repository_provider

    @lru_cache(maxsize=Config.CACHE_MAX_SIZE)
    def get_blueprint(self, type: str) -> Blueprint:
        blueprint: Blueprint = self.blueprint_provider.get_blueprint(type)
        blueprint.realize_extends(self.blueprint_provider.get_blueprint)
        return blueprint

    def invalidate_cache(self):
        logger.warning("Clearing blueprint cache")
        self.get_blueprint.cache_clear()
        self.blueprint_provider.invalidate_cache()

    def save_blob_data(self, node, repository):
        # If the file is created or updated, the blob_reference is a dict.
        if isinstance(node.entity["blob_reference"], dict):
            reference = node.entity["blob_reference"].get("_id")
            file: SpooledTemporaryFile = node.entity["blob_reference"]["file"]
            if not reference:
                uid = str(uuid4())
            reference = f"{repository.name}/{uid}"
            repository.update_blob(uid, file)
            node.entity["size"] = file.seek(0, 2)
        else:
            reference = node.entity["blob_reference"]

        return reference

    def save(self, node: Union[Node, ListNode], data_source_id: str, repository=None, path="") -> Dict:
        """
        Recursively saves a Node.
        Digs down to the leaf child, and based on storageContained,
        either saves the entity and returns the Reference, OR returns the entire entity.
        """
        if not node.entity:
            return {}
        # If not passed a custom repository to save into, use the DocumentService's storage
        if not repository:
            repository: DataSource = self.repository_provider(data_source_id)

        # If the node is a package, we build the path string to be used by filesystem like repositories
        if node.type == DMT.PACKAGE.value:
            path = f"{path}/{node.name}/" if path else f"{node.name}"

        for child in node.children:
            if child.is_array():
                [self.save(x, data_source_id, repository, path) for x in child.children]
            else:
                self.save(child, data_source_id, repository, path)

        if node.type in BLOB_TYPES:
            # Every blueprint of a 'blob_type', has the 'blob_reference' attribute
            node.entity["blob_reference"] = self.save_blob_data(node, repository)

        ref_dict = node.to_ref_dict()

        # If the node is not contained, and has data, save it!
        if not node.storage_contained and ref_dict:
            dto = DTO(ref_dict)
            # Expand this when adding new repositories requiring PATH
            if isinstance(repository, ZipFileClient):
                dto.data["__path__"] = path
            repository.update(dto, node.get_context_storage_attribute())
            return {"_id": node.uid, "type": node.entity["type"], "name": node.name}
        return ref_dict

    def get_by_uid(self, data_source_id: str, document_uid: str, depth: int = 999) -> Node:
        complete_document = get_complete_document(
            document_uid, self.repository_provider(data_source_id), self.get_blueprint, depth
        )

        return Node.from_dict(complete_document, complete_document.get("_id"), blueprint_provider=self.get_blueprint)

    def get_by_path(self, data_source_id: str, directory: str):
        ref_elements = directory.split("/", 1)
        package_name = ref_elements[0]

        package: DTO = self.repository_provider(data_source_id).first(
            {"type": "system/SIMOS/Package", "isRoot": True, "name": package_name}
        )
        if not package:
            raise FileNotFoundException(data_source_id, package_name)

        # TODO: This is slow and unnecessary, step through each document instead, only fetching what is needed.
        complete_document = get_complete_document(
            package.uid, self.repository_provider(data_source_id), self.get_blueprint
        )

        dto = DTO(complete_document)
        node = Node.from_dict(dto.data, dto.uid, blueprint_provider=self.get_blueprint)

        if len(ref_elements) > 1:
            path = ref_elements[1]
            return node.get_by_name_path(path.split("/"))
        else:
            return node

    def get_root_packages(self, data_source_id: str):
        result = self.repository_provider(data_source_id).find({"type": "system/SIMOS/Package", "isRoot": True})
        if not result:
            return []

        return result

    def remove_document(self, data_source_id: str, document_id: str, parent_id: str = None):
        if parent_id:
            parent: Node = self.get_by_uid(data_source_id, parent_id)

            if not parent:
                raise EntityNotFoundException(uid=parent_id)

            attribute_node = parent.search(document_id)

            if not attribute_node:
                raise EntityNotFoundException(uid=document_id)

            if attribute_node.has_uid():
                self._remove_document(data_source_id, document_id)

            attribute_node.remove()

            self.save(parent, data_source_id)

        else:
            self._remove_document(data_source_id, document_id)

    def _remove_document(self, data_source_id, document_id):
        document: Node = self.get_by_uid(data_source_id, document_id)
        if not document:
            raise EntityNotFoundException(uid=document_id)

        # Remove self and children references
        for child in document.traverse():
            # Only remove children if they ARE contained in model and NOT contained in storage
            if child.has_uid() and child.attribute.contained:
                self.repository_provider(data_source_id).delete(child.uid)
                logger.info(f"Deleted document '{child.uid}'")

    def rename_document(self, data_source_id: str, document_id: str, name: str, parent_uid: str = None):
        # Only root-packages have no parent_id
        if not parent_uid:
            root_node: Node = self.get_by_uid(data_source_id, document_id)
            target_node = root_node

        # Grab the parent, and set target based on dotted document_id
        else:
            root_node: Node = self.get_by_uid(data_source_id, parent_uid)
            target_node = root_node.search(document_id)

            if not target_node:
                raise EntityNotFoundException(uid=document_id)

        target_node.entity["name"] = name
        self.save(root_node, data_source_id)

        logger.info(f"Rename document '{target_node.node_id}' to '{name}")

        return {"uid": target_node.node_id}

    def update_document(
        self, data_source_id: str, document_id: str, data: Union[dict, list], attribute_path: str = None
    ):
        root: Node = self.get_by_uid(data_source_id, document_id)
        target_node = root

        # If it's a contained nested node, set the modify target based on dotted-path
        if attribute_path:
            target_node = root.get_by_path(attribute_path.split("."))

        target_node.update(data)
        self.save(root, data_source_id)

        logger.info(f"Updated document '{target_node.node_id}''")
        return {"data": target_node.to_dict()}

    def add_document(
        self, data_source_id: str, parent_id: str, type: str, name: str, description: str, attribute_path: str
    ):
        if not url_safe_name(name):
            raise InvalidDocumentNameException(name)

        root: Node = self.get_by_uid(data_source_id, parent_id)
        if not root:
            raise EntityNotFoundException(uid=parent_id)
        parent: Node = root.get_by_path(attribute_path.split(".")) if attribute_path else root
        if root.attribute.attribute_type != DMT.PACKAGE.value:
            parent.validate_type_on_parent(type)
        # Check if a file/attribute with the same name already exists on the target
        # if duplicate_filename(parent, name):
        if parent.duplicate_attribute(name):
            raise DuplicateFileNameException(data_source_id, f"{parent.name}/{name}")

        entity: Dict = CreateEntity(self.get_blueprint, name=name, type=type, description=description).entity

        if type == SIMOS.BLUEPRINT.value:  # Extend default attributes and uiRecipes
            entity["extends"] = ["system/SIMOS/DefaultUiRecipes", "system/SIMOS/NamedEntity"]

        new_node_id = str(uuid4()) if not parent.storage_contained else ""
        new_node_attribute = BlueprintAttribute(parent.key, type)
        new_node = Node.from_dict(entity, new_node_id, self.get_blueprint, new_node_attribute)

        if isinstance(parent, ListNode):
            new_node.key = str(len(parent.children)) if parent.is_array() else new_node.name
            parent.add_child(new_node)
        # This covers adding a new optional document (not appending to a list)
        else:
            new_node.key = attribute_path.split(".")[-1]
            root.replace(parent.node_id, new_node)

        self.save(root, data_source_id)

        return {"uid": new_node.node_id}

    def remove_by_path(self, data_source_id: str, directory: str):
        # Convert filesystem path to NodeTree path
        tree_path = "/content/".join(directory.split("/"))
        # TODO: Don't fetch complete document when deleting. Should not expect all references to be in place
        root: Node = self.get_by_path(data_source_id, tree_path)
        if not root:
            raise EntityNotFoundException(uid=directory)

        if not root.is_root():  # If not deleting a root package, also remove the reference in the parent
            root.parent.remove_by_path([root.key])
            self.save(root.parent.parent, data_source_id)
        return self._remove_document(data_source_id, root.uid)

    @staticmethod
    def _merge_entity_and_files(node, files):
        """
        Recursively adds the matching posted file to the blob_reference in the node
        """
        if node.type in BLOB_TYPES:
            try:
                node.entity["blob_reference"] = {"file": files[node.entity["blob_reference"]]}
            except KeyError:
                raise KeyError("File referenced in entity does not match any filename posted")
        for node in node.traverse():
            if node.entity:
                for t in node.blueprint.get_blob_types():
                    try:
                        node.entity[t.name]["blob_reference"] = {"file": files[node.entity[t.name]["blob_reference"]]}
                    except KeyError:
                        raise KeyError("File referenced in entity does not match any filename posted")

    # Add entity by path
    def add(self, data_source_id: str, path: str, document: NamedEntity, files: dict):
        target: Node = self.get_by_path(data_source_id, path)
        if not target:
            raise EntityNotFoundException(uid=path)

        new_node_id = str(uuid4()) if not target.storage_contained else ""

        new_node = Node.from_dict(
            {**document.dict()},
            new_node_id,
            self.get_blueprint,
            BlueprintAttribute(name=path.split("/")[-1], attribute_type=document.type),
        )
        self._merge_entity_and_files(new_node, files)

        if isinstance(target, ListNode):
            new_node.parent = target
            target.add_child(new_node)
            self.save(target.parent, data_source_id)
        else:
            new_node.parent = target.parent
            target = new_node
            self.save(target, data_source_id)

        return {"uid": new_node.node_id}

    def search(self, data_source_id, search_data):
        repository: DataSource = self.repository_provider(data_source_id)

        if not isinstance(repository.get_default_repository().client, MongoDBClient):
            raise RepositoryException(
                f"Search is not supported on this repository type; {type(repository.repository).__name__}"
            )

        process_search_data = build_mongo_query(self.get_blueprint, search_data)

        result: List[DTO] = repository.find(process_search_data)
        result_list = {}
        for doc in result:
            result_list[doc.name] = doc.data

        return result_list

    def insert_reference(
        self, data_source_id: str, document_id: str, reference: Reference, attribute_path: str
    ) -> dict:
        root: Node = self.get_by_uid(data_source_id, document_id)
        attribute_node = root.search(f"{document_id}.{attribute_path}")
        if not attribute_node:
            raise EntityNotFoundException(uid=document_id + attribute_path)

        # Check that target exists and has correct values
        # The SIMOS/Entity type can reference any type (used by Package)
        referenced_document: DTO = self.repository_provider(data_source_id).get(reference.uid)
        if not referenced_document:
            raise EntityNotFoundException(uid=data_source_id + reference.uid)
        if DMT.ENTITY.value != attribute_node.type != referenced_document.type:
            raise InvalidEntityException(
                f"The referenced entity should be of type '{attribute_node.type}'"
                f", but was '{referenced_document.type}'"
            )
        if reference.name != referenced_document.name or reference.type != referenced_document.type:
            raise InvalidEntityException(
                f"The 'name' and 'type' values of the reference does not match the referenced document."
                f"'{reference.name}' --> '{referenced_document.name}',"
                f"{reference.type} --> {referenced_document.type}"
            )
        # If the node to update is a list, append to end
        if attribute_node.is_array():
            attribute_node.add_child(
                Node.from_dict(
                    entity={**reference.dict(by_alias=True), "_id": str(reference.uid)},
                    uid=str(reference.uid),
                    blueprint_provider=self.get_blueprint,
                    node_attribute=attribute_node.attribute,
                )
            )
        else:
            attribute_node.entity = {**reference.dict(by_alias=True), "_id": str(reference.uid)}
            attribute_node.uid = str(reference.uid)
        self.save(root, data_source_id)

        logger.info(
            f"Inserted reference to '{referenced_document.name}'({referenced_document.uid})"
            f" as '{attribute_path}' in '{root.name}'({root.uid})"
        )

        return root.to_dict()

    def remove_reference(self, data_source_id: str, document_id: str, attribute_path: str) -> dict:
        root: Node = self.get_by_uid(data_source_id, document_id)
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

        return root.to_dict()

    def create_zip_export(self, absolute_document_ref: str) -> str:
        archive_path = "temp_zip_archive.zip"
        data_source_id, document_uid = absolute_document_ref.split("/", 1)
        document: Node = self.get_by_uid(data_source_id, document_uid)
        # TODO: Is this secure?
        with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
            # Save the selected node, using custom ZipFile repository
            self.save(document, data_source_id, ZipFileClient(zip_file))
        return archive_path
