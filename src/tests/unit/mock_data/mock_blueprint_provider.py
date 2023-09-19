import json
from typing import List

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class MockBlueprintProvider:
    def __init__(
        self,
        mock_blueprint_folder: str,
        simos_blueprints_available_for_test: List[str] = None,
    ):
        if simos_blueprints_available_for_test is None:
            simos_blueprints_available_for_test = []
        if mock_blueprint_folder.endswith("/"):
            mock_blueprint_folder = mock_blueprint_folder[:-1]
        self.mock_blueprint_folder = mock_blueprint_folder
        self.simos_blueprints_available_for_test = simos_blueprints_available_for_test

    def get_blueprint(self, type: str):
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
            with open(f"{self.mock_blueprint_folder}/{type}.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type in self.simos_blueprints_available_for_test:
            return Blueprint(file_repository_test.get(type), type)
        raise FileNotFoundError(
            f"Invalid type {type} provided to the MockBlueprintProvider. No such blueprint found in the test data."
        )
