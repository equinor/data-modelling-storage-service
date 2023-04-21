import unittest

from common.utils.create_entity import CreateEntity
from domain_classes.blueprint import Blueprint
from domain_classes.dimension import Dimension
from enums import SIMOS
from services.document_service import DocumentService
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_utils import mock_storage_recipe_provider

basic_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "A box",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "name"},
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "type"},
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "description"},
        {"attributeType": "integer", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "length"},
    ],
}

higher_rank_array_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Higher rank integer arrays",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "name"},
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "type"},
        {"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "description"},
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
            return Blueprint(higher_rank_array_blueprint)
        elif template_type == "basic_blueprint":
            return Blueprint(basic_blueprint)
        else:
            return Blueprint(file_repository_test.get(template_type))


document_service = DocumentService(
    recipe_provider=mock_storage_recipe_provider, repository_provider=None, blueprint_provider=BlueprintProvider()
)
blueprint_provider = document_service.get_blueprint


class DefaultArrayTestCase(unittest.TestCase):
    def test_creation_of_default_array_simple(self):
        default_array = Dimension("*", "integer").create_default_array(blueprint_provider, CreateEntity)

        assert default_array == []

    def test_creation_of_default_array_complex_type(self):
        default_array = Dimension("1,1", "dmss://system/SIMOS/Package").create_default_array(
            blueprint_provider, CreateEntity
        )

        assert default_array == [
            [{"name": "", "type": "dmss://system/SIMOS/Package", "_meta_": {}, "isRoot": False, "content": []}]
        ]

    def test_creation_of_default_array_unfixed_rank2(self):
        default_array = Dimension("*,*", "integer").create_default_array(blueprint_provider, CreateEntity)

        assert default_array == [[]]

    def test_creation_of_default_array_fixed_rank2(self):
        default_array = Dimension("2,1", "integer").create_default_array(blueprint_provider, CreateEntity)
        # fmt: off
        assert default_array == [
            [0],
            [0],
        ]
        # fmt: on

    def test_creation_of_default_array_mixed_rank_string(self):
        default_array = Dimension("2,*,3", "string").create_default_array(blueprint_provider, CreateEntity)
        # fmt: off
        assert default_array == [
            [["", "", ""]],
            [["", "", ""]],
        ]
        # fmt: on

    def test_creation_of_default_array_mixed_rank3_int(self):
        default_array = Dimension("2,2,*", "integer").create_default_array(blueprint_provider, CreateEntity)
        expected = [[[], []], [[], []]]

        assert default_array == expected

    def test_creation_of_default_array_mixed_rank3_bool(self):
        default_array = Dimension("1,2,1", "boolean").create_default_array(blueprint_provider, CreateEntity)
        expected = [[[False], [False]]]

        assert default_array == expected


if __name__ == "__main__":
    unittest.main()
