import unittest
from unittest import mock

from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_blueprint_provider import blueprint_provider
from utils.data_structure.compare import pretty_eq
from utils.exceptions import (
    DuplicateFileNameException,
    EntityNotFoundException,
    InvalidChildTypeException,
    InvalidEntityException,
)


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
        if type == "base_child":  # A very basic blueprint, extends from NamedEntity
            return Blueprint(
                DTO(
                    {
                        "name": "BaseChild",
                        "type": "system/SIMOS/Blueprint",
                        "extends": ["system/SIMOS/NamedEntity"],
                        "attributes": [
                            {"name": "AValue", "attributeType": "integer", "type": "system/SIMOS/BlueprintAttribute",},
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

        doc_1_after = {
            "_id": "1",
            "name": "Parent",
            "description": "Test",
            "type": "blueprint_with_optional_attr",
            "im_optional": {},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

        node: Node = document_service.get_by_uid("testing", "1")
        node.update(doc_1_after)
        document_service.save(node, "testing")

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None

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

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.add_document(
            "testing", "1", "blueprint_2", "new_entity", "This is my new entity", "im_optional"
        )

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None

    def test_add_invalid_child_type(self):
        repository = mock.Mock()

        doc_storage = {"1": {"_id": "1", "name": "parent", "description": "", "type": "parent", "SomeChild": {},}}

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=MultiTypeBlueprintProvider(), repository_provider=lambda x: repository
        )
        with self.assertRaises(InvalidChildTypeException):
            document_service.update_document(
                data_source_id="testing",
                document_id="1",
                attribute_path="SomeChild",
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

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return repository

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )
        document_service.add_document(
            "testing", "1", "blueprint_2", "new_entity", "This is my new entity", "nested_with_optional.im_optional"
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
                "im_optional": {"name": "duplicate", "description": "", "type": "blueprint_2",},
            }
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, storage_attribute):
            doc_storage[dto.uid] = dto.data
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
        )

        with self.assertRaises(DuplicateFileNameException):
            document_service.add_document("testing", "1", "blueprint_2", "duplicate", "This is my new entity", "")

    # def test_insert_reference(self):
    #     repository = mock.Mock()
    #
    #     doc_storage = {
    #         "1": {
    #             "_id": "1",
    #             "name": "Parent",
    #             "description": "",
    #             "type": "uncontained_blueprint",
    #             "uncontained_in_every_way": {},
    #         },
    #         "something": {"_id": "something", "name": "something", "description": "", "type": "blueprint_2",},
    #     }
    #
    #     def mock_get(document_id: str):
    #         return DTO(doc_storage[document_id])
    #
    #     def mock_update(dto: DTO, storage_attribute):
    #         doc_storage[dto.uid] = dto.data
    #         return None
    #
    #     repository.get = mock_get
    #     repository.update = mock_update
    #     document_service = DocumentService(
    #         blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
    #     )
    #
    #     document_service.update_document(
    #         "testing",
    #         document_id="1",
    #         data={"_id": "something", "name": "something", "type": "blueprint_2"},
    #         attribute_path="uncontained_in_every_way",
    #         reference=True,
    #     )
    #     assert doc_storage["1"]["uncontained_in_every_way"] == {
    #         "_id": "something",
    #         "name": "something",
    #         "type": "blueprint_2",
    #     }
    #
    # def test_insert_reference_target_does_not_exist(self):
    #     repository = mock.Mock()
    #
    #     doc_storage = {
    #         "1": {
    #             "_id": "1",
    #             "name": "Parent",
    #             "description": "",
    #             "type": "uncontained_blueprint",
    #             "uncontained_in_every_way": {},
    #         }
    #     }
    #
    #     def mock_get(document_id: str):
    #         try:
    #             return DTO(doc_storage[document_id])
    #         except KeyError:
    #             raise EntityNotFoundException(f"{document_id} was not found in the 'test' data-sources lookupTable")
    #
    #     def mock_update(dto: DTO, storage_attribute):
    #         doc_storage[dto.uid] = dto.data
    #         return None
    #
    #     repository.get = mock_get
    #     repository.update = mock_update
    #     document_service = DocumentService(
    #         blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
    #     )
    #
    #     with self.assertRaises(EntityNotFoundException):
    #         document_service.update_document(
    #             "testing",
    #             document_id="1",
    #             data={"_id": "something", "name": "something", "type": "something"},
    #             attribute_path="uncontained_in_every_way",
    #             reference=True,
    #         )
    #
    # def test_insert_reference_target_exists_but_wrong_type(self):
    #     repository = mock.Mock()
    #
    #     doc_storage = {
    #         "1": {
    #             "_id": "1",
    #             "name": "Parent",
    #             "description": "",
    #             "type": "uncontained_blueprint",
    #             "uncontained_in_every_way": {},
    #         },
    #         "2": {
    #             "_id": "2",
    #             "name": "something",
    #             "description": "hgallo",
    #             "type": "ExtendedBlueprint",
    #             "another_value": "hei du",
    #         },
    #     }
    #
    #     def mock_get(document_id: str):
    #         return DTO(doc_storage[document_id])
    #
    #     def mock_update(dto: DTO, storage_attribute):
    #         doc_storage[dto.uid] = dto.data
    #
    #     repository.get = mock_get
    #     repository.update = mock_update
    #     document_service = DocumentService(
    #         blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
    #     )
    #
    #     with self.assertRaises(InvalidEntityException):
    #         document_service.update_document(
    #             "testing",
    #             document_id="1",
    #             data={"_id": "2", "name": "something", "type": "wrong_type"},
    #             attribute_path="uncontained_in_every_way",
    #             reference=True,
    #         )
    #
    # def test_insert_reference_too_many_attributes(self):
    #     repository = mock.Mock()
    #
    #     doc_storage = {
    #         "1": {
    #             "_id": "1",
    #             "name": "Parent",
    #             "description": "",
    #             "type": "uncontained_blueprint",
    #             "uncontained_in_every_way": {},
    #         },
    #         "2": {"_id": "2", "name": "something", "description": "", "type": "blueprint_2",},
    #     }
    #
    #     def mock_get(document_id: str):
    #         return DTO(doc_storage[document_id])
    #
    #     def mock_update(dto: DTO, storage_attribute):
    #         doc_storage[dto.uid] = dto.data
    #         return None
    #
    #     repository.get = mock_get
    #     repository.update = mock_update
    #     document_service = DocumentService(
    #         blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
    #     )
    #
    #     document_service.update_document(
    #         "testing",
    #         document_id="1",
    #         data={
    #             "_id": "2",
    #             "name": "something",
    #             "type": "blueprint_2",
    #             "description": "hallO",
    #             "something": "something",
    #         },
    #         attribute_path="uncontained_in_every_way",
    #         reference=True,
    #     )
    #     assert doc_storage["1"]["uncontained_in_every_way"] == {
    #         "_id": "2",
    #         "name": "something",
    #         "type": "blueprint_2",
    #     }
    #
    # def test_insert_reference_missing_required_attribute(self):
    #     repository = mock.Mock()
    #
    #     doc_storage = {
    #         "1": {
    #             "_id": "1",
    #             "name": "Parent",
    #             "description": "",
    #             "type": "uncontained_blueprint",
    #             "uncontained_in_every_way": {},
    #         }
    #     }
    #
    #     def mock_get(document_id: str):
    #         return DTO(doc_storage[document_id])
    #
    #     def mock_update(dto: DTO, storage_attribute):
    #         doc_storage[dto.uid] = dto.data
    #         return None
    #
    #     repository.get = mock_get
    #     repository.update = mock_update
    #     document_service = DocumentService(
    #         blueprint_provider=blueprint_provider, repository_provider=lambda x: repository
    #     )
    #
    #     with self.assertRaises(InvalidEntityException):
    #         document_service.update_document(
    #             "testing",
    #             document_id="1",
    #             data={"_id": "something", "type": "something"},
    #             attribute_path="uncontained_in_every_way",
    #             reference=True,
    #         )
