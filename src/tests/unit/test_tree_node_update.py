import unittest
from unittest import mock

from domain_classes.user import User

from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_blueprint_provider import blueprint_provider
from utils.data_structure.compare import pretty_eq
from utils.exceptions import DuplicateFileNameException, InvalidChildTypeException


class MultiTypeBlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "parent":  # Just a container
            return Blueprint(
                DTO(
                    {
                        "name": "Parent",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {
                                "name": "SomeChild",
                                "attributeType": "base_child",
                                "type": "system/SIMOS/BlueprintAttribute",
                                "optional": True,
                            },
                        ],
                    }
                )
            )
        if type == "parent_w_list":  # Just a container with a list
            return Blueprint(
                DTO(
                    {
                        "name": "Parent",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {
                                "name": "SomeChild",
                                "attributeType": "base_child",
                                "type": "system/SIMOS/BlueprintAttribute",
                                "optional": True,
                                "dimensions": "*",
                            },
                        ],
                    }
                )
            )
        if type == "wrapps_parent_w_list":  # Wrapps a uncontained parent_w_list
            return Blueprint(
                DTO(
                    {
                        "name": "wrapps_parent_w_list",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {
                                "name": "Parent-w-list",
                                "attributeType": "parent_w_list",
                                "type": "system/SIMOS/BlueprintAttribute",
                            },
                        ],
                    }
                )
            )
        if type == "base_child":  # A very basic blueprint, extends from NamedEntity
            return Blueprint(
                DTO(
                    {
                        "name": "BaseChild",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {
                                "name": "AValue",
                                "attributeType": "integer",
                                "type": "system/SIMOS/BlueprintAttribute",
                            },
                        ],
                    }
                )
            )
        if type == "special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            return Blueprint(
                DTO(
                    {
                        "name": "SpecialChild",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["base_child"],
                        "attributes": [
                            {
                                "name": "AnExtraValue",
                                "attributeType": "string",
                                "type": "system/SIMOS/BlueprintAttribute",
                            },
                        ],
                    }
                )
            )
        if type == "extra_special_child":  # A blueprint that extends from 'base_child', and adds an extra attribute
            return Blueprint(
                DTO(
                    {
                        "name": "ExtraSpecialChild",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity", "special_child"],
                        "attributes": [
                            {
                                "name": "AnotherExtraValue",
                                "attributeType": "boolean",
                                "type": "system/SIMOS/BlueprintAttribute",
                            },
                        ],
                    }
                )
            )
        if type == "special_child_no_inherit":  # A duplicate of the 'special_child', but does not extends 'base_child'
            return Blueprint(
                DTO(
                    {
                        "name": "SpecialChild",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {
                                "name": "AnExtraValue",
                                "attributeType": "string",
                                "type": "system/SIMOS/BlueprintAttribute",
                            },
                        ],
                    }
                )
            )
        else:
            return Blueprint(DTO(LocalFileRepository().get(type)))


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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

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
            "im_optional": {"name": "new_entity", "type": "blueprint_2", "description": "This is my new entity"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.add_document(
            "testing/1.im_optional",
            data={"type": "blueprint_2", "name": "new_entity", "description": "This is my new entity"},
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
        )
        with self.assertRaises(InvalidChildTypeException):
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
                "im_optional": {"name": "new_entity", "type": "blueprint_2", "description": "This is my new entity"},
            },
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.add_document(
            "testing/1.nested_with_optional.im_optional",
            {"name": "new_entity", "description": "This is my new entity", "type": "blueprint_2"},
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
                    "type": "blueprint_2",
                },
            }
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        with self.assertRaises(DuplicateFileNameException):
            document_service.add_document(
                "testing/1.im_optional",
                data={"type": "blueprint_2", "name": "duplicate", "description": "This is my new entity"},
            )

    def test_add_valid_specialized_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "parent", "SomeChild": {}}}

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
        )

        with self.assertRaises(InvalidChildTypeException) as error:
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
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x, y: repository
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
