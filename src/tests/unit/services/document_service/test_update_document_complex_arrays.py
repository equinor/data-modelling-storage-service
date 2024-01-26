import unittest
from copy import deepcopy
from unittest import mock

from authentication.models import User
from common.address import Address
from features.document.use_cases.update_document_use_case import (
    update_document_use_case,
)
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service
from tests.unit.mocks.mock_recipe_provider import MockStorageRecipeProvider


class ArraysDocumentServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/Entity", "dmss://system/SIMOS/NamedEntity"]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/arrays"
        mock_blueprints_and_file_names = {
            "basic": "basic.blueprint.json",
            "package": "package.blueprint.json",
            "higher_rank_array": "higher_rank_array.blueprint.json",
        }
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        recipe_provider = MockStorageRecipeProvider(
            "src/tests/unit/services/document_service/mock_blueprints/arrays/mock_storage_recipes.json"
        ).provider
        self.mock_document_service = get_mock_document_service(
            blueprint_provider=mock_blueprint_provider, recipe_provider=recipe_provider
        )

    def test_update_complex_array(self):
        # fmt: off
        doc_storage: dict = {
            "1": {
                "_id": "1",
                "name": "complexArraysEntity",
                "type": "higher_rank_array",
                "1_dim-unfixed": [],
                "1_dim-fixed_complex_type": [
                    {
                        "name": "0",
                        "type": "basic",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "1",
                        "type": "basic",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "2",
                        "type": "basic",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "3",
                        "type": "basic",
                        "description": "",
                        "length": 0
                    },
                    {
                        "name": "4",
                        "type": "basic",
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
        document_repository.name = "testing"
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        self.mock_document_service.data_source = repository_provider

        # fmt: off
        data = {
            "_id": "1",
            "name": "complexArraysEntity",
            "type": "higher_rank_array",
            "1_dim-unfixed": [45, 65, 999999999999999999, 0, -12],
            "1_dim-fixed_complex_type": [
                {
                    "name": "0",
                    "type": "basic",
                    "description": "",
                    "length": 1
                },
                {
                    "name": "1",
                    "type": "basic",
                    "description": "",
                    "length": 23
                },
                {
                    "name": "2",
                    "type": "basic",
                    "description": "",
                    "length": 200
                },
                {
                    "name": "3",
                    "type": "basic",
                    "description": "",
                    "length": 345
                },
                {
                    "name": "4",
                    "type": "basic",
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
            document_service=self.mock_document_service
        )

        expected_1 = {
            "_id": "1",
            "name": "complexArraysEntity",
            "type": "higher_rank_array",
            "1_dim-unfixed": [45, 65, 999999999999999999, 0, -12],
            "1_dim-fixed_complex_type": [
                    {
                        "name": "0",
                        "type": "basic",
                        "description": "",
                        "length": 1
                    },
                    {
                        "name": "1",
                        "type": "basic",
                        "description": "",
                        "length": 23
                    },
                    {
                        "name": "2",
                        "type": "basic",
                        "description": "",
                        "length": 200
                    },
                    {
                        "name": "3",
                        "type": "basic",
                        "description": "",
                        "length": 345
                    },
                    {
                        "name": "4",
                        "type": "basic",
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
