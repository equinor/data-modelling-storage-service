import unittest
from copy import deepcopy
from unittest import mock, skip

from authentication.models import User
from common.address import Address
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint import Blueprint
from enums import SIMOS
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_utils import get_mock_document_service

package_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Package",
    "description": "This is a blueprint for a package that contains documents and other packages",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {"attributeType": "boolean", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "isRoot"},
        {
            "attributeType": "object",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "content",
            "dimensions": "*",
            "optional": True,
        },
    ],
}

basic_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "A box",
    "description": "First blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {"attributeType": "integer", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "length"},
    ],
}

higher_rank_array_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Higher rank integer arrays",
    "description": "First blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "integer",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "1_dim-unfixed",
            "dimensions": "*",
        },
        {
            "attributeType": "basic_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "1_dim-fixed_complex_type",
            "dimensions": "5",
        },
        {
            "attributeType": "integer",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "2_dim-unfixed",
            "dimensions": "*,*",
        },
        {
            "attributeType": "integer",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "3_dim-mix",
            "dimensions": "*,1,100",
        },
    ],
}

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    def get_blueprint(self, template_type: str):
        if template_type == "higher_rank_array":
            blueprint = Blueprint(higher_rank_array_blueprint)
        elif template_type == "package_blueprint":
            blueprint = Blueprint(package_blueprint)
        elif template_type == "basic_blueprint":
            blueprint = Blueprint(basic_blueprint)
        else:
            blueprint = Blueprint(file_repository_test.get(template_type))
        blueprint.path = template_type
        return blueprint


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
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider, blueprint_provider=blueprint_provider)
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

        assert get_and_print_diff(doc_storage["1"], expected_1) == []
        assert get_and_print_diff(doc_storage[list(doc_storage)[1]], expected_2) == []

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
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider, blueprint_provider=blueprint_provider)
        # fmt: off
        data = {
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
        update_document_use_case(
            data=data,
            address=Address.from_absolute("dmss://testing/$1"),
            document_service=document_service
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
