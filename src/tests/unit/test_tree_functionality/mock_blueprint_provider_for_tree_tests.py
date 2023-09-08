import json

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        FILE_PATH = "src/tests/unit/test_tree_functionality/mock_blueprints_for_tree_tests/"
        if type in [
            "AreaWithOptionalGarden",
            "BaseChild",
            "Box",
            "Bush",
            "Case",
            "ChestWithOptionalBoxInside",
            "FormBlueprint",
            "Garden",
            "NestedField",
            "Parent",
            "ParentWithListOfChildren",
            "ParentWithListOfChildren",
            "Signal",
            "SignalContainer",
            "SpecialChild",
            "SpecialChildNoInherit",
            "WrappsParentWithList",
            "all_contained_cases_blueprint",
            "recursive",
            "uncontained_list_blueprint",
            "RoomWithOptionalChestInside",
            "ExtraSpecialChild",
        ]:
            with open(FILE_PATH + type + ".blueprint.json") as f:
                return Blueprint(json.load(f), type)
        if type == "blueprint_4":
            with open(FILE_PATH + "Blueprint4.blueprint.json") as f:
                return Blueprint(json.load(f))
        if "system/SIMOS/Reference" in type:
            with open(FILE_PATH + "Reference.blueprint.json") as f:
                return Blueprint(json.load(f))
        if "recursive_blueprint" in type:
            with open(FILE_PATH + "recursive.blueprint.json") as f:
                return Blueprint(json.load(f))
        if type in ["dmss://system/SIMOS/Package", "dmss://system/SIMOS/NamedEntity"]:
            return Blueprint(file_repository_test.get(type), type)

        raise Exception(f"Invalid type {type}")


blueprint_provider = BlueprintProvider()
