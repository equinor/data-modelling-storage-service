from typing import Dict, Union

from core.enums import DMT
from core.repository.repository_exceptions import EntityNotFoundException
from core.repository.repository_factory import get_repository
from core.service.document_service import DocumentService
from core.use_case.utils.generate_index_menu_actions import get_node_on_select
from core.use_case.utils.set_index_context_menu import create_context_menu
from utils.logging import logger
from classes.recipe import RecipePlugin
from classes.tree_node import Node, ListNode
from config import Config


def get_parent_id(data_source_id: str, node: Union[Node, ListNode]):
    if node.parent:
        # Adjust parent, since we skipped content node
        if node.parent.parent and node.parent.parent.type == DMT.PACKAGE.value:
            return node.parent.parent.node_id
        return node.parent_node_id
    else:
        return data_source_id


def get_error_node(data_source_id: str, node: Union[Node]) -> Dict:
    return {
        "parentId": get_parent_id(data_source_id, node),
        "title": node.name,
        "id": node.node_id,
        "nodeType": "document-node",
        "children": [],
        "type": node.type,
        "meta": {
            "menuItems": [],
            "onSelect": {},
            "error": True,
            "isRootPackage": node.is_root(),
            "isList": node.is_array(),
        },
    }


def get_node(node: Union[Node], data_source_id: str, app_settings: dict, document_service) -> Dict:
    menu_items = create_context_menu(node, data_source_id, app_settings, document_service.blueprint_provider)

    children = []
    if node.type == DMT.PACKAGE.value:
        # Skip content node
        if node.has_children():
            # Content node is always the only node in package
            content_node = node.children[0]
            children = [child.node_id for child in content_node.children if is_visible(child)]
    else:
        children = [child.node_id for child in node.children if is_visible(child)]

    return {
        "parentId": get_parent_id(data_source_id, node),
        "title": node.name,
        "id": node.node_id,
        "nodeType": "document-node",
        "children": children,
        "type": node.type,
        "meta": {
            "menuItems": menu_items,
            "onSelect": get_node_on_select(data_source_id, node)
            if node.is_single() and node.type != DMT.PACKAGE.value and node.type != "datasource"
            else {},
            "error": False,
            "isRootPackage": node.is_root() if node.is_single() else False,
            "isList": node.is_array(),
            "dataSource": data_source_id,
        },
    }


def is_visible(node):
    if node.is_root():
        return True
    elif node.is_complex_array():
        return False

    if node.parent.blueprint is None:
        return True

    ui_recipe = node.parent.blueprint.get_ui_recipe_from_blueprint(name="INDEX")
    is_visible = ui_recipe.is_contained(
        node.parent.key if node.parent.is_array() else node.key,
        node.attribute_type,
        node.is_array(),
        RecipePlugin.INDEX
    )
    print(node.node_id, is_visible)
    return is_visible


def extend_index_with_node_tree(
        root: Union[Node, ListNode], data_source_id: str, app_settings: dict, document_service
):
    index = {}

    for node in root.traverse():
        try:
            # Skip package's content node
            if node.parent and node.parent.type == DMT.PACKAGE.value:
                continue

            if not is_visible(node):
                continue

            if node.has_error:
                index[node.node_id] = get_error_node(data_source_id, node)
            else:
                index[node.node_id] = get_node(node, data_source_id, app_settings, document_service)

        except Exception as error:
            logger.exception(error)
            logger.warning(f"Caught error while processing document: {error}")
    return index


class GenerateIndexUseCase:
    def __init__(self, repository_provider=get_repository):
        self.repository_provider = repository_provider

    def execute(self, data_source_id: str, application_page: str) -> dict:
        app_settings = (
            Config.DMT_APPLICATION_SETTINGS if application_page == "blueprints" else Config.ENTITY_APPLICATION_SETTINGS
        )
        document_service = DocumentService(repository_provider=self.repository_provider)
        # make sure we're generating the index with correct blueprints.
        document_service.invalidate_cache()
        root_packages = document_service.get_root_packages(data_source_id=data_source_id)
        root = Node(
            key="root",
            uid=data_source_id,
            entity={"type": "datasource", "name": data_source_id},
            blueprint_provider=document_service.blueprint_provider,
        )
        for root_package in root_packages:
            try:
                root.add_child(
                    document_service.get_by_uid(data_source_id=data_source_id, document_uid=root_package.uid)
                )
            except EntityNotFoundException as error:
                logger.exception(error, "unhandled exception.")
                error_node: Node = Node(
                    key=root_package.uid,
                    uid=root_package.uid,
                    entity={"name": root_package.name, "type": ""},
                    blueprint_provider=document_service.blueprint_provider,
                )
                error_node.set_error(f"failed to add root package {root_package.name} to the root node")
                root.add_child(error_node)
            except Exception as error:
                logger.exception(error, "unhandled exception.")

        return extend_index_with_node_tree(root, data_source_id, app_settings, document_service)

    def single(self, data_source_id: str, document_id: str, application_page: str, parent_id: str) -> Dict:
        app_settings = (
            Config.DMT_APPLICATION_SETTINGS if application_page == "blueprints" else Config.ENTITY_APPLICATION_SETTINGS
        )
        document_service = DocumentService(repository_provider=self.repository_provider)
        # make sure we're generating the index with correct blueprints.
        document_service.invalidate_cache()
        parent_uid = parent_id.split(".", 1)[0]
        if data_source_id == parent_uid:
            document_uid = document_id
        else:
            document_uid = parent_uid

        parent = document_service.get_by_uid(data_source_id=data_source_id, document_uid=document_uid)
        if not parent and data_source_id != document_id:
            raise EntityNotFoundException(uid=parent_id)
        node = parent.search(document_id)
        if not node:
            raise EntityNotFoundException(uid=document_id)
        return extend_index_with_node_tree(node, data_source_id, app_settings, document_service)
