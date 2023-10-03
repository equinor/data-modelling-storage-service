import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.address import Address
from common.exceptions import BadRequestException, ValidationException
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.tree_node import Node
from enums import REFERENCE_TYPES, SIMOS
from features.document.use_cases.add_document_use_case import add_document_use_case
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service
from tests.unit.tree_functionality.mock_data_for_tree_tests.get_node_for_tree_tests import (
    get_form_example_node,
)


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/NamedEntity"]
        mock_blueprint_folder = (
            "src/tests/unit/tree_functionality/mock_data_for_tree_tests/mock_blueprints_for_tree_tests"
        )
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

        def mock_get(document_id: str):
            return deepcopy(self.doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            self.doc_storage[entity["_id"]] = entity
            return None

        self.repository = mock.Mock()
        self.repository.get = mock_get
        self.repository.update = mock_update
        self.doc_storage = {}

        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )

        def repository_provider(data_source_id, user: User):
            return self.repository

        self.mock_document_service = get_mock_document_service(
            blueprint_provider=self.mock_blueprint_provider, repository_provider=repository_provider
        )

    def test_update_single_optional_complex(self):
        chest = {
            "_id": "1",
            "name": "TreasureChest",
            "description": "",
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
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "ChestWithOptionalBoxInside",
                "box": {},
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "ChestWithOptionalBoxInside",
            "box": {"name": "box", "type": "Box", "description": "box"},
        }

        add_document_use_case(
            address=Address("$1.box", "testing"),
            document={"type": "Box", "name": "box", "description": "box"},
            document_service=self.mock_document_service,
        )
        assert get_and_print_diff(self.doc_storage["1"], doc_1_after) == []

    def test_add_invalid_child_type(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "description": "",
                "type": "Parent",
                "SomeChild": {},
            }
        }

        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data={"name": "whatever", "type": "SpecialChildNoInherit", "AnExtraValue": "Hallo there!"},
                address=Address("$1.SomeChild", "testing"),
                document_service=self.mock_document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'"
        )
        assert not self.doc_storage["1"]["SomeChild"]

    def test_add_optional_nested(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "RoomWithOptionalChestInside",
                "chest": {
                    "name": "chest",
                    "description": "",
                    "type": "ChestWithOptionalBoxInside",
                    "box": {},
                },
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "RoomWithOptionalChestInside",
            "chest": {
                "name": "chest",
                "description": "",
                "type": "ChestWithOptionalBoxInside",
                "box": {
                    "name": "box",
                    "type": "Box",
                    "description": "box",
                },
            },
        }
        add_document_use_case(
            address=Address("$1.chest.box", "testing"),
            document={"name": "box", "description": "box", "type": "Box"},
            document_service=self.mock_document_service,
        )

        assert get_and_print_diff(self.doc_storage["1"], doc_1_after) == []

    def test_add_duplicate(self):
        self.doc_storage = {
            "1": {
                "_id": "1",
                "name": "chest",
                "description": "",
                "type": "ChestWithOptionalBoxInside",
                "box": {
                    "name": "duplicate",
                    "description": "",
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
        self.doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "Parent", "SomeChild": {}}}

        update_document_use_case(
            data={"name": "whatever", "type": "SpecialChild", "AnExtraValue": "Hallo there!", "AValue": 13},
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )

        assert self.doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "SpecialChild",
            "AnExtraValue": "Hallo there!",
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type(self):
        self.doc_storage = {"1": {"_id": "1", "name": "Parent", "description": "", "type": "Parent", "SomeChild": {}}}

        update_document_use_case(
            data={
                "name": "whatever",
                "type": "ExtraSpecialChild",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )
        assert self.doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "ExtraSpecialChild",
            "AnExtraValue": "Hallo there!",
            "AnotherExtraValue": True,
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type_to_list_attribute(self):
        self.doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "ParentWithListOfChildren", "SomeChild": []}
        }

        update_document_use_case(
            data=[
                {"name": "whatever", "type": "SpecialChild", "AnExtraValue": "Hallo there!", "AValue": 13},
                {
                    "name": "whatever",
                    "type": "ExtraSpecialChild",
                    "AnExtraValue": "Hallo there!",
                    "AnotherExtraValue": True,
                    "AValue": 13,
                },
            ],
            address=Address("$1.SomeChild", "testing"),
            document_service=self.mock_document_service,
        )

        assert self.doc_storage["1"]["SomeChild"] == [
            {"name": "whatever", "type": "SpecialChild", "AnExtraValue": "Hallo there!", "AValue": 13},
            {
                "name": "whatever",
                "type": "ExtraSpecialChild",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
        ]

    def test_add_invalid_child_type_to_list_attribute(self):
        self.doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "ParentWithListOfChildren", "SomeChild": []}
        }

        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data=[
                    {"name": "whatever", "type": "SpecialChild", "AnExtraValue": "Hallo there!", "AValue": 13},
                    {
                        "name": "whatever",
                        "type": "SpecialChildNoInherit",
                        "AnExtraValue": "Hallo there!",
                    },
                ],
                address=Address("$1.SomeChild", "testing"),
                document_service=self.mock_document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'"
        )
        assert self.doc_storage["1"]["SomeChild"] == []

    def test_add_child_with_empty_list(self):
        self.doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "WrappsParentWithList", "Parent-w-list": {}}
        }

        data = {
            "_id": "1",
            "name": "parent",
            "description": "",
            "type": "WrappsParentWithList",
            "Parent-w-list": {"name": "whatever", "type": "ParentWithListOfChildren", "SomeChild": []},
        }
        update_document_use_case(
            data=data, address=Address("$1", "testing"), document_service=self.mock_document_service
        )

        assert self.doc_storage["1"]["Parent-w-list"]["SomeChild"] == []

    def test_set_update_uncontained_child(self):
        form_node = get_form_example_node()
        target_node = form_node.children[1]
        new_reference = {"type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value, "address": "$new"}
        target_node.update(new_reference)
        assert "_id" not in target_node.entity and target_node.entity["address"] == "$new"
