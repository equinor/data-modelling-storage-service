import unittest

from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.dimension import Dimension
from features.entity.use_cases.instantiate_entity_use_case.create_entity import (
    CreateEntity,
)
from features.entity.use_cases.instantiate_entity_use_case.create_entity_arrays import (
    create_default_array,
    remove_first_and_join,
)
from services.document_service.document_service import DocumentService
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_recipe_provider import MockStorageRecipeProvider


class DefaultArrayTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = [
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Entity",
            "dmss://system/SIMOS/AttributeTypes",
            "dmss://system/SIMOS/Package",
            "dmss://system/SIMOS/BlueprintAttribute",
        ]
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names={},
            mock_blueprint_folder="",
            simos_blueprints_available_for_test=simos_blueprints,
        )
        recipe_provider = MockStorageRecipeProvider(
            "src/tests/unit/mocks/mock_storage_recipes/mock_storage_recipes.json"
        ).provider
        document_service = DocumentService(
            recipe_provider=recipe_provider,
            repository_provider=None,
            blueprint_provider=mock_blueprint_provider,
        )
        self.blueprint_provider = document_service.get_blueprint

    def test_creation_of_array_simple(self):
        default_array = create_default_array(Dimension("*", "integer"), self.blueprint_provider, CreateEntity)
        assert default_array == []

    def test_creation_of_array_simple_with_default_value(self):
        integer_blueprint_attribute_with_default = BlueprintAttribute(
            name="", attribute_type="integer", default=[22, 33, 44]
        )
        default_array = create_default_array(
            Dimension("*", "integer"),
            self.blueprint_provider,
            CreateEntity,
            integer_blueprint_attribute_with_default.default,
        )

        assert default_array == integer_blueprint_attribute_with_default.default

    def test_creation_of_default_array_complex_type(self):
        empty_string_blueprint_attribute = BlueprintAttribute(name="", attribute_type="string")

        default_array = create_default_array(
            Dimension("1,1", "dmss://system/SIMOS/Package"),
            self.blueprint_provider,
            CreateEntity,
            empty_string_blueprint_attribute,
        )

        assert default_array == [
            [
                {
                    "name": "",
                    "type": "dmss://system/SIMOS/Package",
                    "isRoot": False,
                    "content": [],
                }
            ]
        ]

    def test_creation_of_default_array_unfixed_rank2(self):
        default_array = create_default_array(Dimension("*,*", "integer"), self.blueprint_provider, CreateEntity)

        assert default_array == [[]]

    def test_creation_of_default_array_fixed_rank2(self):
        default_array = create_default_array(Dimension("2,1", "integer"), self.blueprint_provider, CreateEntity)
        # fmt: off
        assert default_array == [
            [0],
            [0],
        ]
        # fmt: on

    def test_creation_of_default_array_mixed_rank_string(self):
        default_array = create_default_array(Dimension("2,*,3", "string"), self.blueprint_provider, CreateEntity)
        # fmt: off
        assert default_array == [
            [["", "", ""]],
            [["", "", ""]],
        ]
        # fmt: on

    def test_creation_of_default_array_mixed_rank3_int(self):
        default_array = create_default_array(Dimension("2,2,*", "integer"), self.blueprint_provider, CreateEntity)
        expected: list = [[[], []], [[], []]]

        assert default_array == expected

    def test_creation_of_default_array_mixed_rank3_bool(self):
        default_array = create_default_array(Dimension("1,2,1", "boolean"), self.blueprint_provider, CreateEntity)
        expected = [[[False], [False]]]

        assert default_array == expected

    def test_remove_first_and_join(self):
        assert remove_first_and_join(["1", "2", "3", "4"]) == "2,3,4"
        assert remove_first_and_join(["0", "0"]) == "0"
        assert remove_first_and_join(["0"]) == ""
        assert remove_first_and_join([]) == ""


if __name__ == "__main__":
    unittest.main()
