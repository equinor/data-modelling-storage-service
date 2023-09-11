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
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.get_node_for_tree_tests import (
    get_form_example_node,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_blueprint_provider_for_tree_tests import (
    BlueprintProvider,
)
from tests.unit.test_tree_functionality.mock_data_for_tree_tests.mock_document_service_for_tree_tests import (
    get_mock_document_service_for_tree_tests,
)


class DocumentServiceTestCase(unittest.TestCase):
    def test_update_single_optional_complex(self):
        repository = mock.Mock()

        chest = {
            "_id": "1",
            "name": "TreasureChest",
            "description": "",
            "type": "ChestWithOptionalBoxInside",
            "im_optional": {},
        }

        doc_storage = {"1": chest}

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(repository_provider)

        node: Node = document_service.get_document(Address("$1", "testing"))
        node.update(
            {
                "_id": "1",
                "name": "Parent",
                "description": "Test",
                "type": "ChestWithOptionalBoxInside",
                "box": {},
            }
        )
        document_service.save(node, "testing")

        assert doc_storage["1"]["box"] == {}

    def test_add_optional(self):
        repository = mock.Mock()

        doc_storage = {
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

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(repository_provider)
        add_document_use_case(
            address=Address("$1.box", "testing"),
            document={"type": "Box", "name": "box", "description": "box"},
            update_uncontained=True,
            document_service=document_service,
        )
        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []

    def test_add_invalid_child_type(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "parent",
                "description": "",
                "type": "Parent",
                "SomeChild": {},
            }
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            blueprint_provider=BlueprintProvider, repository_provider=lambda x, y: repository
        )
        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data={"name": "whatever", "type": "SpecialChildNoInherit", "AnExtraValue": "Hallo there!"},
                address=Address("$1.SomeChild", "testing"),
                document_service=document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'"
        )
        assert not doc_storage["1"]["SomeChild"]

    def test_add_optional_nested(self):
        repository = mock.Mock()

        doc_storage = {
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

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(repository_provider)
        add_document_use_case(
            address=Address("$1.chest.box", "testing"),
            document={"name": "box", "description": "box", "type": "Box"},
            update_uncontained=True,
            document_service=document_service,
        )

        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []

    def test_add_duplicate(self):
        repository = mock.Mock()

        doc_storage = {
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

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(lambda x, y: repository)

        with self.assertRaises(BadRequestException):
            add_document_use_case(
                address=Address("$1.box", "testing"),
                document={"type": "Box", "name": "duplicate", "description": "box"},
                update_uncontained=True,
                document_service=document_service,
            )

    def test_add_valid_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "Parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            lambda id, user: repository, blueprint_provider=BlueprintProvider()
        )
        update_document_use_case(
            data={"name": "whatever", "type": "SpecialChild", "AnExtraValue": "Hallo there!", "AValue": 13},
            address=Address("$1.SomeChild", "testing"),
            document_service=document_service,
        )

        assert doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "SpecialChild",
            "AnExtraValue": "Hallo there!",
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "Parent", "description": "", "type": "Parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            lambda id, user: repository, blueprint_provider=BlueprintProvider()
        )
        update_document_use_case(
            data={
                "name": "whatever",
                "type": "ExtraSpecialChild",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
            address=Address("$1.SomeChild", "testing"),
            document_service=document_service,
        )
        assert doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "ExtraSpecialChild",
            "AnExtraValue": "Hallo there!",
            "AnotherExtraValue": True,
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type_to_list_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "ParentWithListOfChildren", "SomeChild": []}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            lambda id, user: repository, blueprint_provider=BlueprintProvider()
        )
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
            document_service=document_service,
        )

        assert doc_storage["1"]["SomeChild"] == [
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
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "ParentWithListOfChildren", "SomeChild": []}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            lambda id, user: repository, blueprint_provider=BlueprintProvider()
        )

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
                document_service=document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'BaseChild' (or extending from it). Got 'SpecialChildNoInherit'"
        )
        assert doc_storage["1"]["SomeChild"] == []

    def test_add_child_with_empty_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "WrappsParentWithList", "Parent-w-list": {}}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service_for_tree_tests(
            lambda id, user: repository, blueprint_provider=BlueprintProvider()
        )

        data = {
            "_id": "1",
            "name": "parent",
            "description": "",
            "type": "WrappsParentWithList",
            "Parent-w-list": {"name": "whatever", "type": "ParentWithListOfChildren", "SomeChild": []},
        }
        update_document_use_case(data=data, address=Address("$1", "testing"), document_service=document_service)

        assert doc_storage["1"]["Parent-w-list"]["SomeChild"] == []

    def test_set_update_uncontained_child(self):
        form_node = get_form_example_node()
        target_node = form_node.children[1]
        new_reference = {"type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value, "address": "$new"}
        target_node.update(new_reference)
        assert "_id" not in target_node.entity and target_node.entity["address"] == "$new"
