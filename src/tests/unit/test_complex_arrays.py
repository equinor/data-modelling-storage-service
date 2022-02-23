import unittest
from unittest import mock, skip

from authentication.models import User

from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from services.document_service import DocumentService
from storage.repositories.file import LocalFileRepository
from utils.data_structure.compare import pretty_eq
from enums import SIMOS

package_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Package",
    "description": "This is a blueprint for a package that contains documents and other packages",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"attributeType": "boolean", "type": "system/SIMOS/BlueprintAttribute", "name": "isRoot"},
        {
            "attributeType": "object",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "content",
            "dimensions": "*",
            "optional": True,
        },
    ],
    "storageRecipes": [
        {
            "type": "system/SIMOS/StorageRecipe",
            "name": "DefaultStorageRecipe",
            "description": "",
            "attributes": [{"name": "content", "type": "object", "contained": False}],
        }
    ],
}

basic_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "A box",
    "description": "First blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"attributeType": "integer", "type": "system/SIMOS/BlueprintAttribute", "name": "length"},
    ],
}

higher_rank_array_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Higher rank integer arrays",
    "description": "First blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "1_dim-unfixed",
            "dimensions": "*",
        },
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "1_dim-fixed_complex_type",
            "dimensions": "5",
        },
        {
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "2_dim-unfixed",
            "dimensions": "*,*",
        },
        {
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "3_dim-mix",
            "dimensions": "*,1,100",
        },
    ],
}

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    def get_blueprint(self, template_type: str):
        if template_type == "higher_rank_array":
            return Blueprint(DTO(higher_rank_array_blueprint))
        elif template_type == "package_blueprint":
            return Blueprint(DTO(package_blueprint))
        elif template_type == "basic_blueprint":
            return Blueprint(DTO(basic_blueprint))
        else:
            return Blueprint(DTO(file_repository_test.get(template_type)))


blueprint_provider = BlueprintProvider()


class ArraysDocumentServiceTestCase(unittest.TestCase):
    @skip
    def test_create_complex_array(self):
        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Package",
                "description": "My package",
                "type": SIMOS.PACKAGE.value,
                "content": [],
            }
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.add_document(
            data_source_id="testing",
            parent_id="1",
            data={"type": "higher_rank_array", "name": "complexArraysEntity"},
            attribute_path="content",
        )

        expected_1 = {"_id": "1", "content": [{"name": "complexArraysEntity", "type": "higher_rank_array"}]}
        # Disable Black formatting for the matrix
        # fmt: off
        expected_2 = {
            "name": "complexArraysEntity",
            "type": "higher_rank_array",
            "1_dim-unfixed": [],
            "1_dim-fixed_complex_type": [
                {
                 "name": "0",
                 "type": "basic_blueprint",
                 "description": "",
                 "length": 0
                },
                {
                    "name": "1",
                    "type": "basic_blueprint",
                    "description": "",
                    "length": 0
                },
                {
                    "name": "2",
                    "type": "basic_blueprint",
                    "description": "",
                    "length": 0
                },
                {
                    "name": "3",
                    "type": "basic_blueprint",
                    "description": "",
                    "length": 0
                },
                {
                    "name": "4",
                    "type": "basic_blueprint",
                    "description": "",
                    "length": 0
                },
            ],
            "2_dim-unfixed": [[]],
            "3_dim-mix": [
                [
                    [
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    ]
                ],
            ],
        }
        # fmt: on

        assert pretty_eq(expected_1, doc_storage["1"]) is None
        assert pretty_eq(expected_2, doc_storage[list(doc_storage)[1]]) is None

    def test_update_complex_array(self):

        # fmt: off
        doc_storage = {
            "1": {
                "_id": "1",
                "name": "complexArraysEntity",
                "type": "higher_rank_array",
                "1_dim-unfixed": [],
                "1_dim-fixed_complex_type": [
                    {
                        "name": "0",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "1",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "2",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "3",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "4",
                        "type": "basic_blueprint",
                        "description": "some description",
                        "length": 0
                    },
                ],
                "2_dim-unfixed": [[], []],
                "3_dim-mix": [
                    [
                        [
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                        ]
                    ],
                ],
            }
        }

        # fmt: on

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        # fmt: off
        document_service.update_document(
            data_source_id="testing",
            dotted_id="1",
            data={
                "_id": "1",
                "name": "complexArraysEntity",
                "type": "higher_rank_array",
                "1_dim-unfixed": [45, 65, 999999999999999999, 0, -12],
                "1_dim-fixed_complex_type": [
                    {
                        "name": "0",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 1
                    },
                    {
                        "name": "1",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 23
                    },
                    {
                        "name": "2",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 200
                    },
                    {
                        "name": "3",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 345
                    },
                    {
                        "name": "4",
                        "type": "basic_blueprint",
                        "description": "some other description",
                        "length": 1
                    },
                ],
                "2_dim-unfixed": [[23, 234, 123], [1, 1, 1, 1, 1, 1]],
                "3_dim-mix": [
                    [
                        [
                            11, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 22
                        ]
                    ],
                    [
                        [
                            33, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 44
                        ]
                    ],
                ],
            },
        )

        expected_1 = {
            "_id": "1",
            "name": "complexArraysEntity",
            "type": "higher_rank_array",
            "1_dim-unfixed": [45, 65, 999999999999999999, 0, -12],
            "1_dim-fixed_complex_type": [
                    {
                        "name": "0",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 1
                    },
                    {
                        "name": "1",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 23
                    },
                    {
                        "name": "2",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 200
                    },
                    {
                        "name": "3",
                        "type": "basic_blueprint",
                        "description": "",
                        "length": 345
                    },
                    {
                        "name": "4",
                        "type": "basic_blueprint",
                        "description": "some other description",
                        "length": 1
                    },
                ],
            "2_dim-unfixed": [[23, 234, 123], [1, 1, 1, 1, 1, 1]],
            "3_dim-mix": [
                [
                    [
                        11, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 22
                    ]
                ],
                [
                    [
                        33, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 44
                    ]
                ],
            ],
        }
        # fmt: on
        assert expected_1 == doc_storage["1"]
