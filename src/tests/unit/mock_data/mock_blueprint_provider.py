import json
from typing import Dict, List

from domain_classes.blueprint import Blueprint
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class MockBlueprintProvider:
    def __init__(
        self,
        mock_blueprint_folder: str,
        mock_blueprints_and_file_names: Dict[str, str],
        simos_blueprints_available_for_test: List[str] = None,
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
                return Blueprint(json.load(f), type)
        if type in self.simos_blueprints_available_for_test:
            return Blueprint(file_repository_test.get(type), type)
        raise FileNotFoundError(
            f"Invalid type {type} asked for from the MockBlueprintProvider. No such blueprint were provided as available blueprints as parameters in the initialisation of the MockBlueprintProvider."
        )
