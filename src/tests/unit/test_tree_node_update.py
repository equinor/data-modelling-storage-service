import unittest
from unittest import mock

from authentication.models import User
from common.exceptions import BadRequestException
from common.utils.data_structure.compare import pretty_eq
from domain_classes.blueprint import Blueprint
from domain_classes.tree_node import Node
from enums import SIMOS
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_utils import get_mock_document_service


class MultiTypeBlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "parent":  # Just a container
            return Blueprint(
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
        if type == "parent_w_list":  # Just a container with a list
            return Blueprint(
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
        if type == "wrapps_parent_w_list":  # Wrapps a uncontained parent_w_list
            return Blueprint(
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
        if type == "base_child":  # A very basic blueprint, extends from NamedEntity
            return Blueprint(
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
        if type == "special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            return Blueprint(
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
        if type == "extra_special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            return Blueprint(
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
        if type == "special_child_no_inherit":  # A duplicate of the 'special_child', but does not extends 'base_child'
            return Blueprint(
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
        else:
            return Blueprint(LocalFileRepository().get(type))


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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(repository_provider)

        node: Node = document_service.get_node_by_uid("testing", "1")
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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(repository_provider)
        document_service.add_document(
            "testing/1.im_optional",
            data={"type": "basic_blueprint", "name": "new_entity", "description": "This is my new entity"},
        )

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None

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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
        )
        with self.assertRaises(BadRequestException):
            document_service.update_document(
                data_source_id="testing",
                dotted_id="1.SomeChild",
                data={"name": "whatever", "type": "special_child_no_inherit", "AnExtraValue": "Hallo there!"},
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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(repository_provider)
        document_service.add_document(
            "testing/1.nested_with_optional.im_optional",
            {"name": "new_entity", "description": "This is my new entity", "type": "basic_blueprint"},
        )

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None

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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        with self.assertRaises(BadRequestException):
            document_service.add_document(
                "testing/1.im_optional",
                data={"type": "basic_blueprint", "name": "duplicate", "description": "This is my new entity"},
            )

    def test_add_valid_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        document_service.update_document(
            data_source_id="testing",
            dotted_id="1.SomeChild",
            data={"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        document_service.update_document(
            data_source_id="testing",
            dotted_id="1.SomeChild",
            data={
                "name": "whatever",
                "type": "extra_special_child",
                "AnExtraValue": "Hallo there!",
                "AnotherExtraValue": True,
                "AValue": 13,
            },
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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )
        document_service.update_document(
            data_source_id="testing",
            dotted_id="1.SomeChild",
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
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )

        with self.assertRaises(BadRequestException) as error:
            document_service.update_document(
                data_source_id="testing",
                dotted_id="1.SomeChild",
                data=[
                    {"name": "whatever", "type": "special_child", "AnExtraValue": "Hallo there!", "AValue": 13},
                    {
                        "name": "whatever",
                        "type": "special_child_no_inherit",
                        "AnExtraValue": "Hallo there!",
                    },
                ],
            )
        print(error.exception)
        assert doc_storage["1"]["SomeChild"] == []

    def test_add_child_with_empty_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {"_id": "1", "name": "parent", "description": "", "type": "wrapps_parent_w_list", "Parent-w-list": {}}
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(
            lambda id, user: repository, blueprint_provider=MultiTypeBlueprintProvider()
        )

        document_service.update_document(
            data_source_id="testing",
            dotted_id="1",
            data={
                "_id": "1",
                "name": "parent",
                "description": "",
                "type": "wrapps_parent_w_list",
                "Parent-w-list": {"name": "whatever", "type": "parent_w_list", "SomeChild": []},
            },
        )
        assert doc_storage["1"]["Parent-w-list"]["SomeChild"] == []
