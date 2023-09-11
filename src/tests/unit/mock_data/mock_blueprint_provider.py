import json

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()

_FILE_PATH = "src/tests/unit/mock_data/mock_blueprints/"


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type in [
            "BaseChild",
            "ExtendedBlueprint",
            "Parent",
            "SecondLevelExtendedBlueprint",
            "SpecialChild",
            "all_contained_cases_blueprint",
            "basic_blueprint",
            "blob",
            "blobContainer",
            "blueprint_with_blob",
            "blueprint_with_nested_optional_attr",
            "blueprint_with_optional_attr",
            "blueprint_with_second_level_nested_uncontained_attribute",
            "blueprint_with_second_level_reference",
            "two_contained_deep_attributes",
            "uncontained_blueprint",
            "uncontained_list_blueprint",
            "FuelPumpTest",
            "CarTest",
            "WheelTest",
            "EngineTest",
            "CarRental",
            "Customer",
            "RentalCar",
        ]:
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type in [
            "dmss://system/SIMOS/AttributeTypes",
            "dmss://system/SIMOS/Blob",
            "dmss://system/SIMOS/Blueprint",
            "dmss://system/SIMOS/BlueprintAttribute",
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Package",
            "dmss://system/SIMOS/Reference",
        ]:
            return Blueprint(file_repository_test.get(type), type)
        raise FileNotFoundError(
            f"Invalid type {type} provided to the MockBlueprintProvider. No such blueprint found in the test data."
        )


blueprint_provider = BlueprintProvider()
