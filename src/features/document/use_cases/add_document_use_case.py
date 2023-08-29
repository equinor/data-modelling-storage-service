from typing import BinaryIO, List, Optional

from fastapi import UploadFile

from common.address import Address
from common.exceptions import (
    BadRequestException,
    NotFoundException,
    ValidationException,
)
from common.tree_node_serializer import tree_node_from_dict
from common.utils.merge_entity_and_files import merge_entity_and_files
from common.utils.validators import validate_entity, validate_entity_against_self
from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.tree_node import ListNode, Node
from enums import SIMOS
from restful.request_types.shared import Entity
from services.document_service import DocumentService


def _add_document_to_data_source(
    data_source_id: str, document: dict, update_uncontained: Optional[bool], document_service: DocumentService
) -> dict:
    """Add the document to an existing data source.

    Args:
       data_source_id: The data source ID
       document: The entity to be added
       update_uncontained: Whether to update uncontained children (deprecated)
       document_service: The document service

    Returns:
       A dict that contains the ID of the added document.
    """

    if document.get("type") != SIMOS.PACKAGE.value and not document.get("isRoot"):
        raise BadRequestException("Only root packages may be added without a parent.")

    new_node = tree_node_from_dict(
        document,
        blueprint_provider=document_service.get_blueprint,
        recipe_provider=document_service.get_storage_recipes,
    )

    try:
        if document_service.get_document(Address(new_node.entity["name"], data_source_id), depth=99):
            raise ValidationException(
                message=f"A root package named '{new_node.entity['name']}' already exists",
                data={"dataSource": data_source_id, "document": document},
            )
    except NotFoundException:
        pass

    new_node.set_uid(new_node.generate_id())

    document_service.save(new_node, data_source_id, update_uncontained=update_uncontained)

    return {"uid": new_node.node_id}


def _add_document_to_entity_or_list(
    address: Address,
    document: dict,
    files: dict[str, BinaryIO] | None,
    update_uncontained: Optional[bool],
    document_service: DocumentService,
) -> dict:
    """Add the document to an existing entity.

    Args:
       address: Reference to an existing entity or to an attribute (complex or list attribute) inside an entity.
       document: The entity to be added
       files: Dict with names and files of the files contained in the document
       update_uncontained: Whether to update uncontained children (deprecated)

    Returns:
       A dict that contains the ID of the added document.
    """
    entity: Entity = Entity(**document)

    try:
        target: Node = document_service.get_document(address, depth=99)
    except NotFoundException:
        target = None

    if not target:
        # If target does not exist, there are 2 cases to consider:
        #   1) the target is an optional attribute that does not exist yet. In that case, we set the target to be
        #      the parent of entity referenced by 'address'.
        #   2) the address is wrong. In that case, raise Exception.

        # It is assumed that address.path is to an attribute, e.g. dataSource/package/document.attribute
        split_address_path: list[str] = address.path.rsplit(".", 1)

        if len(split_address_path) <= 1 and split_address_path[0] == address.path:
            # Raising NotFoundException, since the get_document() did not find the document
            # with address=address.path in the above try except statement
            raise NotFoundException(f"Could not find document {address}")

        parent_address_as_string, last_attribute_in_address = split_address_path

        parent_address: Address = Address(
            protocol=address.protocol, path=parent_address_as_string, data_source=address.data_source
        )
        parent_node: Node = document_service.get_document(parent_address, depth=1)
        parent_blueprint = parent_node.blueprint
        if (
            len(
                [
                    blueprint_attribute
                    for blueprint_attribute in parent_blueprint.attributes
                    if blueprint_attribute.name == last_attribute_in_address
                ]
            )
            == 0
        ):
            raise NotFoundException(
                f"Could not find attribute {last_attribute_in_address} in blueprint for {parent_blueprint.name}"
            )

        parent_document = parent_node.entity
        attribute_to_update = [
            blueprint_attribute
            for blueprint_attribute in parent_blueprint.attributes
            if blueprint_attribute.name == last_attribute_in_address
        ][0]
        if attribute_to_update.is_array:
            parent_document[last_attribute_in_address] = [document]
        else:
            parent_document[last_attribute_in_address] = document

        target = parent_node
        new_node = tree_node_from_dict(
            {**parent_document},
            blueprint_provider=document_service.get_blueprint,
            node_attribute=BlueprintAttribute(name=target.attribute.name, attribute_type=entity.type),
            recipe_provider=document_service.get_storage_recipes,
        )
        document_service.save(new_node, address.data_source, update_uncontained=update_uncontained)

        return {"uid": f"{new_node.node_id}.{last_attribute_in_address}"}

    if target.type != SIMOS.PACKAGE.value and target.type != "object":
        validate_entity(
            document,
            document_service.get_blueprint,
            document_service.get_blueprint(target.attribute.attribute_type),
            "extend",
        )

    new_node = tree_node_from_dict(
        {**document},
        blueprint_provider=document_service.get_blueprint,
        node_attribute=BlueprintAttribute(name=target.attribute.name, attribute_type=entity.type),
        recipe_provider=document_service.get_storage_recipes,
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
        merge_entity_and_files(new_node, files)

    if target.type == SIMOS.PACKAGE.value:
        target = target.children[0]  # Set target to be the packages content

    if isinstance(target, ListNode) or target.parent.type == SIMOS.PACKAGE.value:
        new_node.parent = target
        new_node.key = str(len(target.children))
        if new_node.should_have_id():
            new_node.set_uid(new_node.generate_id())
        target.add_child(new_node)
        document_service.save(target.find_parent(), address.data_source, update_uncontained=False)
    else:
        new_node.parent = target.parent
        target.parent.replace(new_node.node_id, new_node)
        document_service.save(target.find_parent(), address.data_source, update_uncontained=False)

    document_service.save(new_node, address.data_source, update_uncontained=update_uncontained)

    return {"uid": new_node.node_id}


def add_document_use_case(
    document: dict,
    address: Address,
    document_service: DocumentService,
    files: Optional[List[UploadFile]] = None,
    update_uncontained: Optional[bool] = False,
) -> dict:
    """Add document to a data source or existing entity. Can also be used to add (complex) items to a list.

    Args:
        document: The entity to be added
        address: Reference to a package, attribute inside an entity (either a list or a complex attribute) or a data source
        document_service: The document service
        files: Dict with names and files of the files contained in the document
        update_uncontained: Whether to update uncontained children (deprecated)

    Returns:
        A dict that contains the ID of the added document.
    """
    validate_entity_against_self(document, document_service.get_blueprint)

    if not address.path:
        return _add_document_to_data_source(address.data_source, document, update_uncontained, document_service)

    return _add_document_to_entity_or_list(
        address=address,
        document=document,
        files={f.filename: f.file for f in files} if files else None,
        update_uncontained=update_uncontained,
        document_service=document_service,
    )
