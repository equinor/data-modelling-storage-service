import unittest
from unittest import mock

from common.address import Address
from common.tree.tree_node_serializer import tree_node_to_dict
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service


class GetDocumentInputTestCase(unittest.TestCase):
    def setUp(self):
        self.car_rental_company: dict = {
            "_id": "1",
            "type": "CarRental",
            "name": "myCarRentalCompany",
            "cars": [
                {
                    "type": "RentalCar",
                    "name": "Volvo 240",
                    "plateNumber": "123",
                    "engine": {
                        "address": "$2",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                }
            ],
            "customers": [
                {
                    "address": "$4",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                }
            ],
        }
        self.customer: dict = {
            "_id": "4",
            "type": "Customer",
            "name": "Jane",
            "car": {
                "address": "$1.cars[0]",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
        }
        self.engine: dict = {
            "_id": "2",
            "type": "EngineTest",
            "name": "myEngine",
            "description": "",
            "fuelPump": {
                "address": "$3",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
            "power": 120,
        }
        self.fuel_pump: dict = {
            "_id": "3",
            "type": "FuelPumpTest",
            "name": "fuelPump",
            "description": "A standard fuel pump",
        }
        self.document_repository = mock.Mock()
        self.document_repository.name = "datasource"
        self.document_repository.get = self.mock_get
        self.document_repository.find = self.mock_find

        simos_blueprints = ["dmss://system/SIMOS/NamedEntity", "dmss://system/SIMOS/Reference"]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/car_rental_blueprints"
        mock_blueprints_and_file_names = {
            "CarRental": "CarRental.blueprint.json",
            "RentalCar": "RentalCar.blueprint.json",
            "EngineTest": "EngineTest.blueprint.json",
            "FuelPumpTest": "FuelPumpTest.blueprint.json",
            "Customer": "Customer.blueprint.json",
        }
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        self.document_service = get_mock_document_service(
            repository_provider=lambda x, y: self.document_repository, blueprint_provider=mock_blueprint_provider
        )

    def mock_get(self, document_id: str):
        if document_id == "1":
            return {**self.car_rental_company}
        if document_id == "2":
            return {**self.engine}
        if document_id == "3":
            return {**self.fuel_pump}
        if document_id == "4":
            return {**self.customer}
        return None

    def mock_find(self, query: dict) -> list[dict]:
        documents: list[dict] = [self.car_rental_company, self.engine, self.fuel_pump, self.customer]
        for key, value in query.items():
            documents = list(filter(lambda x: key in x and x[key] == value, documents))
        return documents

    def test_query_no_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1.customers(name=Jane)"), 0)
        )
        self.assertDictEqual(root, self.car_rental_company["customers"][0])

    def test_query_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1.customers(name=Jane)"), 1)
        )
        self.assertDictEqual(root, self.customer)

    def test_depth_0(self):
        root = tree_node_to_dict(self.document_service.get_document(Address.from_absolute("datasource/$1"), 0))
        self.assertDictEqual(root, self.car_rental_company)

    def test_depth_2(self):
        root = tree_node_to_dict(self.document_service.get_document(Address.from_absolute("datasource/$1"), 2))
        self.assertDictEqual(root, {**self.car_rental_company, "customers": [self.customer]})

    def test_depth_3(self):
        root = tree_node_to_dict(self.document_service.get_document(Address.from_absolute("datasource/$1"), 3))
        self.assertDictEqual(
            root,
            {
                **self.car_rental_company,
                "cars": [{**self.car_rental_company["cars"][0], "engine": self.engine}],
                "customers": [{**self.customer, "car": self.car_rental_company["cars"][0]}],
            },
        )

    def test_nested_depth_0(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1.cars[0].engine"), 0)
        )
        self.assertDictEqual(root, self.car_rental_company["cars"][0]["engine"])

    def test_nested_depth_1(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1.cars[0].engine"), 1)
        )
        self.assertDictEqual(root, self.engine)

    def test_nested_depth_2(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1.cars[0].engine"), 2)
        )
        self.assertDictEqual(root, {**self.engine, "fuelPump": self.fuel_pump})
