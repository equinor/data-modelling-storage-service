import json

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()

_FILE_PATH = "src/tests/unit/mock_data/mock_blueprints/"


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "all_contained_cases_blueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "basic_blueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_with_second_level_reference":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "two_contained_deep_attributes":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "ExtendedBlueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "SecondLevelExtendedBlueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "uncontained_blueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "uncontained_list_blueprint":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_with_second_level_nested_uncontained_attribute":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_with_optional_attr":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_with_nested_optional_attr":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blob":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blobContainer":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_with_blob":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/FuelPumpTest":
            with open(_FILE_PATH + "FuelPumpTest.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/EngineTest":
            with open(_FILE_PATH + "EngineTest.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/CarTest":
            with open(_FILE_PATH + "CarTest.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/WheelTest":
            with open(_FILE_PATH + "WheelTest.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/CarRental":
            with open(_FILE_PATH + "CarRental.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/RentalCar":
            with open(_FILE_PATH + "RentalCar.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "test_data/complex/Customer":
            with open(_FILE_PATH + "Customer.blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "Parent":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "BaseChild":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "SpecialChild":
            with open(_FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        else:
            return Blueprint(file_repository_test.get(type), type)


blueprint_provider = BlueprintProvider()
