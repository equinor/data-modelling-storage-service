import unittest
from copy import deepcopy
from unittest import mock

from common.address import Address
from features.document.use_cases.check_exsistence_use_case import (
    check_existence_use_case,
)
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class CheckExistenceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = {
            "1": {
                "name": "Test_document",
                "type": "basic_blueprint",
                "_id": "1",
            }
        }
        self.repository = mock.Mock()
        self.repository.get = self.mock_get
        self.repository.delete = self.mock_delete

        simos_blueprints = ["dmss://system/SIMOS/NamedEntity"]
        mock_blueprint_folder = "src/tests/unit/mock_data/mock_blueprints"
        mock_blueprints_and_file_names = {"basic_blueprint": "basic_blueprint.blueprint.json"}
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        self.document_service = get_mock_document_service(
            repository_provider=lambda x, y: self.repository, blueprint_provider=mock_blueprint_provider
        )

    def mock_get(self, document_id: str):
        return deepcopy(self.storage.get(document_id))

    def mock_delete(self, document_id: str):
        del self.storage[document_id]

    def test_check_existence_of_existing_document(self):
        assert (
            check_existence_use_case(address=Address("$1", "testing"), document_service=self.document_service) is True
        )

    def test_check_existence_of_non_existing_document(self):
        assert (
            check_existence_use_case(address=Address("$2", "testing"), document_service=self.document_service) is False
        )
