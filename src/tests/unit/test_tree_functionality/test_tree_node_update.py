import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.address import Address
from common.exceptions import BadRequestException, ValidationException
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint import Blueprint
from domain_classes.tree_node import Node
from enums import REFERENCE_TYPES, SIMOS
from features.document.use_cases.add_document_use_case import add_document_use_case
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_data.mock_document_service import get_mock_document_service
from tests.unit.test_tree_functionality.get_node_for_tree_tests import (
    get_form_example_node,
)


class MultiTypeBlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        blueprint = None
        if type == "parent":  # Just a container
            blueprint = Blueprint(
                {
                    "name": "Parent",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value],
                    "attributes": [
                        {
                            "name": "SomeChild",
                            "attributeType": "base_child",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                            "optional": True,
                        },
                    ],
                }
            )
        elif type == "parent_w_list":  # Just a container with a list
            blueprint = Blueprint(
                {
                    "name": "Parent",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value],
                    "attributes": [
                        {
                            "name": "SomeChild",
                            "attributeType": "base_child",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                            "optional": True,
                            "dimensions": "*",
                        },
                    ],
                }
            )
        elif type == "wrapps_parent_w_list":  # Wrapps a uncontained parent_w_list
            blueprint = Blueprint(
                {
                    "name": "wrapps_parent_w_list",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value],
                    "attributes": [
                        {
                            "name": "Parent-w-list",
                            "attributeType": "parent_w_list",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                        },
                    ],
                }
            )
        elif type == "base_child":  # A very basic blueprint, extends from NamedEntity
            blueprint = Blueprint(
                {
                    "name": "BaseChild",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value],
                    "attributes": [
                        {
                            "name": "AValue",
                            "attributeType": "integer",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                        },
                    ],
                }
            )
        elif type == "special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            blueprint = Blueprint(
                {
                    "name": "SpecialChild",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": ["base_child"],
                    "attributes": [
                        {
                            "name": "AnExtraValue",
                            "attributeType": "string",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                        },
                    ],
                }
            )
        elif type == "extra_special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            blueprint = Blueprint(
                {
                    "name": "ExtraSpecialChild",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value, "special_child"],
                    "attributes": [
                        {
                            "name": "AnotherExtraValue",
                            "attributeType": "boolean",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                        },
                    ],
                }
            )
        elif (
            type == "special_child_no_inherit"
        ):  # A duplicate of the 'special_child', but does not extends 'base_child'
            blueprint = Blueprint(
                {
                    "name": "SpecialChild",
                    "type": SIMOS.BLUEPRINT.value,
                    "extends": [SIMOS.NAMED_ENTITY.value],
                    "attributes": [
                        {
                            "name": "AnExtraValue",
                            "attributeType": "string",
                            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
                        },
                    ],
                }
            )
        elif type == "FormBlueprint":
            return Blueprint(
                {
                    "name": "FormBlueprint",
                    "type": "system/SIMOS/Blueprint",
                    "attributes": [
                        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "inputEntity",
                            "description": "Generic input entity",
                            "attributeType": "object",
                            "contained": False,
                        },
                    ],
                }
            )
        else:
            blueprint = Blueprint(LocalFileRepository().get(type))

        blueprint.path = type
        return blueprint


class DocumentServiceTestCase(unittest.TestCase):
    def test_update_single_optional_complex(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_optional_attr",
                "im_optional": {},
            }
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
        document_service = get_mock_document_service(repository_provider)

        node: Node = document_service.get_document(Address("$1", "testing"))
        node.update(
            {
                "_id": "1",
                "name": "Parent",
                "description": "Test",
                "type": "blueprint_with_optional_attr",
                "im_optional": {},
            }
        )
        document_service.save(node, "testing")

        assert doc_storage["1"]["im_optional"] == {}

    def test_add_optional(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_optional_attr",
                "im_optional": {},
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_optional_attr",
            "im_optional": {"name": "new_entity", "type": "basic_blueprint", "description": "This is my new entity"},
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
        document_service = get_mock_document_service(repository_provider)
        add_document_use_case(
            address=Address("$1.im_optional", "testing"),
            document={"type": "basic_blueprint", "name": "new_entity", "description": "This is my new entity"},
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
                "type": "parent",
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
        document_service = get_mock_document_service(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
        )
        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data={"name": "whatever", "type": "special_child_no_inherit", "AnExtraValue": "Hallo there!"},
                address=Address("$1.SomeChild", "testing"),
                document_service=document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'base_child' (or extending from it). Got 'special_child_no_inherit'"
        )
        assert not doc_storage["1"]["SomeChild"]

    def test_add_optional_nested(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_nested_optional_attr",
                "nested_with_optional": {
                    "name": "Parent",
                    "description": "",
                    "type": "blueprint_with_optional_attr",
                    "im_optional": {},
                },
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_nested_optional_attr",
            "nested_with_optional": {
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_optional_attr",
                "im_optional": {
                    "name": "new_entity",
                    "type": "basic_blueprint",
                    "description": "This is my new entity",
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
        document_service = get_mock_document_service(repository_provider)
        add_document_use_case(
            address=Address("$1.nested_with_optional.im_optional", "testing"),
            document={"name": "new_entity", "description": "This is my new entity", "type": "basic_blueprint"},
            update_uncontained=True,
            document_service=document_service,
        )

        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []

    def test_add_duplicate(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_optional_attr",
                "im_optional": {
                    "name": "duplicate",
                    "description": "",
                    "type": "basic_blueprint",
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
        document_service = get_mock_document_service(lambda x, y: repository)

        with self.assertRaises(BadRequestException):
            add_document_use_case(
                address=Address("$1.im_optional", "testing"),
                document={"type": "basic_blueprint", "name": "duplicate", "description": "This is my new entity"},
                update_uncontained=True,
                document_service=document_service,
            )

    def test_add_valid_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        update_document_use_case(
            data={"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
            address=Address("$1.SomeChild", "testing"),
            document_service=document_service,
        )

        assert doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "special_child",
            "AnExtraValue": "Hallo there!",
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        update_document_use_case(
            data={
                "name": "whatever",
                "type": "extra_special_child",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
            address=Address("$1.SomeChild", "testing"),
            document_service=document_service,
        )
        assert doc_storage["1"]["SomeChild"] == {
            "name": "whatever",
            "type": "extra_special_child",
            "AnExtraValue": "Hallo there!",
            "AnotherExtraValue": True,
            "AValue": 13,
        }

    def test_add_valid_second_level_specialized_child_type_to_list_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "parent_w_list", "SomeChild": []}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        update_document_use_case(
            data=[
                {"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
                {
                    "name": "whatever",
                    "type": "extra_special_child",
                    "AnExtraValue": "Hallo there!",
                    "AnotherExtraValue": True,
                    "AValue": 13,
                },
            ],
            address=Address("$1.SomeChild", "testing"),
            document_service=document_service,
        )

        assert doc_storage["1"]["SomeChild"] == [
            {"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
            {
                "name": "whatever",
                "type": "extra_special_child",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
        ]

    def test_add_invalid_child_type_to_list_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "parent_w_list", "SomeChild": []}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )

        with self.assertRaises(ValidationException) as error:
            update_document_use_case(
                data=[
                    {"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
                    {
                        "name": "whatever",
                        "type": "special_child_no_inherit",
                        "AnExtraValue": "Hallo there!",
                    },
                ],
                address=Address("$1.SomeChild", "testing"),
                document_service=document_service,
            )
        assert (
            error.exception.message
            == "Entity should be of type 'base_child' (or extending from it). Got 'special_child_no_inherit'"
        )
        assert doc_storage["1"]["SomeChild"] == []

    def test_add_child_with_empty_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "wrapps_parent_w_list", "Parent-w-list": {}}
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )

        data = {
            "_id": "1",
            "name": "parent",
            "description": "",
            "type": "wrapps_parent_w_list",
            "Parent-w-list": {"name": "whatever", "type": "parent_w_list", "SomeChild": []},
        }
        update_document_use_case(data=data, address=Address("$1", "testing"), document_service=document_service)

        assert doc_storage["1"]["Parent-w-list"]["SomeChild"] == []

    def test_set_update_uncontained_child(self):
        form_node = get_form_example_node()
        target_node = form_node.children[1]
        new_reference = {"type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value, "address": "$new"}
        target_node.update(new_reference)
        assert "_id" not in target_node.entity and target_node.entity["address"] == "$new"
