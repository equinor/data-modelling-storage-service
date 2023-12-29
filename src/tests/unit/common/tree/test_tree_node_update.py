import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.address import Address
from common.exceptions import BadRequestException, ValidationException
from common.tree.tree_node import Node
from common.tree.tree_node_serializer import tree_node_from_dict
from enums import REFERENCE_TYPES, SIMOS
from features.document.use_cases.add_document_use_case import add_document_use_case
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from tests.unit.common.tree.mock_data.get_mock_nodes import get_form_example_node
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service
from tests.unit.mocks.mock_recipe_provider import MockStorageRecipeProvider


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = [
            "dmss://system/SIMOS/Entity",
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Reference",
            "dmss://system/SIMOS/Blueprint",
            "dmss://system/SIMOS/BlueprintAttribute",
        ]
        mock_blueprint_folder = "src/tests/unit/common/tree/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {
            "Bush": "Bush.blueprint.json",
            "Box": "Box.blueprint.json",
            "ChestWithOptionalBoxInside": "ChestWithOptionalBoxInside.blueprint.json",
            "RoomWithOptionalChestInside": "RoomWithOptionalChestInside.blueprint.json",
            "SpecialChild": "SpecialChild.blueprint.json",
            "SpecialChildNoInherit": "SpecialChildNoInherit.blueprint.json",
            "ExtraSpecialChild": "ExtraSpecialChild.blueprint.json",
            "Parent": "Parent.blueprint.json",
            "ParentWithListOfChildren": "ParentWithListOfChildren.blueprint.json",
            "WrappsParentWithList": "WrappsParentWithList.blueprint.json",
            "BaseChild": "BaseChild.blueprint.json",
        }
        self.form_node = get_form_example_node(mock_blueprint_folder, mock_blueprints_and_file_names, simos_blueprints)

        def mock_get(document_id: str):
            return deepcopy(self.doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            self.doc_storage[entity["_id"]] = entity
            return None

        self.repository = mock.Mock()
        self.repository.get = mock_get
        self.repository.update = mock_update
        self.doc_storage: dict = {}

        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )

        def repository_provider(data_source_id, user: User):
            return self.repository

        mock_recipe_folder = "src/tests/unit/common/tree/mock_data/mock_storage_recipes.json"
        recipe_provider = MockStorageRecipeProvider(mock_recipe_folder).provider
        self.mock_document_service = get_mock_document_service(
            blueprint_provider=self.mock_blueprint_provider,
            repository_provider=repository_provider,
            recipe_provider=recipe_provider,
        )

    def test_update_single_optional_complex(self):
        chest = {
            "_id": "1",
            "name": "TreasureChest",
            "type": "ChestWithOptionalBoxInside",
        }
        self.doc_storage = {"1": chest}
        node: Node = self.mock_document_service.get_document(Address("$1", "data-source"))
        node.update(
            {
                "_id": "1",
                "name": "Updated",
                "description": "Test",
                "type": "ChestWithOptionalBoxInside",
                "box": {},
            }
        )
        self.mock_document_service.save(node, "data-source")

        assert self.doc_storage["1"]["type"] == "ChestWithOptionalBoxInside"
        assert self.doc_storage["1"]["name"] == "Updated"
        assert len(self.doc_storage) == 1

    def test_add_optional(self):
        entity: dict = {
            "_id": "1",
            "name": "Parent",
            "type": "ChestWithOptionalBoxInside",
        }
        self.doc_storage = {"1": deepcopy(entity)}

        entity_after = deepcopy(entity)
        entity_after["box"] = {"name": "box", "type": "Box", "description": "box"}

        add_document_use_case(
            address=Address("$1.box", "testing"),
            document={"type": "Box", "name": "box", "description": "box"},
            document_service=self.mock_document_service,
        )
        self.assertEqual(self.doc_storage["1"], entity_after)

    def test_add_invalid_child_type(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "type": "Parent",
                "SomeChild": {},
            }
        }

        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data={
                    "name": "whatever",
                    "type": "SpecialChildNoInherit",
                    "AnExtraValue": "Hallo there!",
                },
                address=Address("$1.SomeChild", "testing"),
                document_service=self.mock_document_service,
            )
        self.assertEqual(
            error.exception.message,
            "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'",
        )
        self.assertDictEqual(self.doc_storage["1"]["SomeChild"], {})

    def test_add_optional_nested(self):
        entity: dict = {
            "_id": "1",
            "name": "Parent",
            "type": "RoomWithOptionalChestInside",
            "chest": {
                "name": "chest",
                "type": "ChestWithOptionalBoxInside",
            },
        }

        self.doc_storage = {"1": deepcopy(entity)}

        entity_after = deepcopy(entity)
        entity_after["chest"]["box"] = {
            "name": "box",
            "type": "Box",
            "description": "box",
        }

        add_document_use_case(
            address=Address("$1.chest.box", "testing"),
            document={"name": "box", "description": "box", "type": "Box"},
            document_service=self.mock_document_service,
        )

        self.assertDictEqual(self.doc_storage["1"], entity_after)

    def test_update_blueprint_attribute_default_with_int(self):
        blueprint = self.mock_blueprint_provider.get_blueprint("Box").to_dict()
        blueprint_node = tree_node_from_dict(blueprint, self.mock_blueprint_provider.get_blueprint)
        attribute_node = blueprint_node.get_by_path(["attributes", "0"])

        new_value = {
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "method",
            "description": "What method to call inside runnable.tsx",
            "attributeType": "number",
            "default": 67,
        }
        attribute_node.update(new_value)
        self.assertEqual(attribute_node.entity["default"], 67)

    def test_update_blueprint_attribute_default_with_dict(self):
        blueprint = self.mock_blueprint_provider.get_blueprint("Box").to_dict()
        blueprint_node = tree_node_from_dict(blueprint, self.mock_blueprint_provider.get_blueprint)
        attribute_node = blueprint_node.get_by_path(["attributes", "0"])

        new_value = {
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "method",
            "description": "What method to call inside runnable.tsx",
            # There is no check if default value matches 'attributeType' in node.update(). It should happen before...
            "attributeType": "number",
            "default": {"type": "test"},
        }
        attribute_node.update(new_value)
        self.assertDictEqual(attribute_node.entity["default"], {"type": "test"})

    def test_update_blueprint_attribute_default_with_bool(self):
        blueprint = self.mock_blueprint_provider.get_blueprint("Box").to_dict()
        blueprint_node = tree_node_from_dict(blueprint, self.mock_blueprint_provider.get_blueprint)
        attribute_node = blueprint_node.get_by_path(["attributes", "0"])

        new_value = {
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "method",
            "description": "What method to call inside runnable.tsx",
            "attributeType": "number",
            "default": True,
        }
        attribute_node.update(new_value)
        self.assertEqual(attribute_node.entity["default"], True)

    def test_add_duplicate(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "chest",
                "type": "ChestWithOptionalBoxInside",
                "box": {
                    "name": "duplicate",
                    "type": "Box",
                },
            }
        }

        with self.assertRaises(BadRequestException):
            add_document_use_case(
                address=Address("$1.box", "testing"),
                document={"type": "Box", "name": "duplicate", "description": "box"},
                document_service=self.mock_document_service,
            )

    def test_add_valid_specialized_child_type(self):
        entity = {"_id": "1", "name": "parent", "type": "Parent", "SomeChild": {}}
        child = {
            "name": "whatever",
            "type": "SpecialChild",
            "AnExtraValue": "Hallo there!",
            "AValue": 13,
        }

        self.doc_storage = {"1": deepcopy(entity)}

        update_document_use_case(
            data=deepcopy(child),
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )

        self.assertDictEqual(
            self.doc_storage["1"]["SomeChild"],
            child,
        )

    def test_add_valid_second_level_specialized_child_type(self):
        self.doc_storage = {"1": {"_id": "1", "name": "Parent", "type": "Parent", "SomeChild": {}}}
        child = {
            "name": "whatever",
            "type": "ExtraSpecialChild",
            "AnExtraValue": "Hallo there!",
            "AnotherExtraValue": True,
            "AValue": 13,
        }
        update_document_use_case(
            data=deepcopy(child),
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )
        self.assertDictEqual(self.doc_storage["1"]["SomeChild"], child)

    def test_add_valid_second_level_specialized_child_type_to_list_attribute(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "type": "ParentWithListOfChildren",
                "SomeChild": [],
            }
        }
        child_list = [
            {
                "name": "whatever",
                "type": "SpecialChild",
                "AnExtraValue": "Hallo there!",
                "AValue": 13,
            },
            {
                "name": "whatever",
                "type": "ExtraSpecialChild",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
        ]
        update_document_use_case(
            data=deepcopy(child_list),
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )

        self.assertListEqual(self.doc_storage["1"]["SomeChild"], child_list)

    def test_add_invalid_child_type_to_list_attribute(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "type": "ParentWithListOfChildren",
                "SomeChild": [],
            }
        }
        invalid_child_list = [
            {
                "name": "whatever",
                "type": "SpecialChild",
                "AnExtraValue": "Hallo there!",
                "AValue": 13,
            },
            {
                "name": "whatever",
                "type": "SpecialChildNoInherit",
                "AnExtraValue": "Hallo there!",
            },
        ]
        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data=invalid_child_list,
                address=Address("$1.SomeChild", "testing"),
                document_service=self.mock_document_service,
            )
        self.assertEqual(
            error.exception.message,
            "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'",
        )
        self.assertListEqual(self.doc_storage["1"]["SomeChild"], [])

    def test_add_child_with_empty_list(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "type": "WrappsParentWithList",
                "Parent-w-list": {},
            }
        }
        child = {
            "_id": "1",
            "name": "parent",
            "type": "WrappsParentWithList",
            "Parent-w-list": {
                "name": "whatever",
                "type": "ParentWithListOfChildren",
                "SomeChild": [],
            },
        }
        update_document_use_case(
            data=child,
            address=Address("$1", "testing"),
            document_service=self.mock_document_service,
        )
        self.assertEqual(self.doc_storage["1"]["Parent-w-list"]["type"], "ParentWithListOfChildren")
        self.assertListEqual(self.doc_storage["1"]["Parent-w-list"]["SomeChild"], [])

    def test_set_update_uncontained_child(self):
        target_node = self.form_node.children[1]
        new_reference = {
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
            "address": "$new",
        }
        target_node.update(new_reference)
        assert "_id" not in target_node.entity and target_node.entity["address"] == "$new"
