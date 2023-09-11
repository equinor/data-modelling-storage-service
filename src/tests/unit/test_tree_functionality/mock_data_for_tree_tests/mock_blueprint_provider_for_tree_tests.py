import json

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        FILE_PATH = "src/tests/unit/test_tree_functionality/mock_data_for_tree_tests/mock_blueprints_for_tree_tests/"
        if type in [
            "AreaWithOptionalGarden",
            "BaseChild",
            "Blueprint4",
            "Box",
            "Bush",
            "Case",
            "ChestWithOptionalBoxInside",
            "ExtraSpecialChild",
            "FormBlueprint",
            "Garden",
            "NestedField",
            "Parent",
            "ParentWithListOfChildren",
            "ParentWithListOfChildren",
            "Recursive",
            "RoomWithOptionalChestInside",
            "Signal",
            "SignalContainer",
            "SpecialChild",
            "SpecialChildNoInherit",
            "WrappsParentWithList",
            "all_contained_cases_blueprint",
            "uncontained_list_blueprint",
        ]:
            with open(FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type in ["dmss://system/SIMOS/Reference", "dmss://system/SIMOS/Package", "dmss://system/SIMOS/NamedEntity"]:
            return Blueprint(file_repository_test.get(type), type)

        raise Exception(f"Invalid type {type}")


blueprint_provider = BlueprintProvider()
