import json

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class MockBlueprintProvider:
    def __init__(
        self,
        mock_blueprint_folder: str,
        mock_blueprints_and_file_names: dict[str, str],
        simos_blueprints_available_for_test: list[str] = None,
    ):
        if simos_blueprints_available_for_test is None:
            simos_blueprints_available_for_test = []
        if mock_blueprint_folder.endswith("/"):
            mock_blueprint_folder = mock_blueprint_folder[:-1]
        self.mock_blueprint_folder = mock_blueprint_folder
        self.mock_blueprints_and_file_names = mock_blueprints_and_file_names
        self.simos_blueprints_available_for_test = simos_blueprints_available_for_test

    def get_blueprint(self, type: str):
        if file_name := self.mock_blueprints_and_file_names.get(type):
            with open(f"{self.mock_blueprint_folder}/{file_name}") as f:
                bp = Blueprint(json.load(f), type)
                bp.realize_extends(self.get_blueprint)
                return bp
        if type in self.simos_blueprints_available_for_test:
            bp = Blueprint(file_repository_test.get(type), type)
            bp.realize_extends(self.get_blueprint)
            return bp
        raise FileNotFoundError(
            f"Invalid type {type} asked for from the MockBlueprintProvider. No such blueprint were provided as available blueprints as parameters in the initialisation of the MockBlueprintProvider."
        )
