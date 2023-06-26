import unittest
from unittest import mock

from common.address import Address
from common.tree_node_serializer import tree_node_to_dict
from common.utils.data_structure.compare import get_and_print_diff
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_utils import get_mock_document_service


class GetDocumentInputTestCase(unittest.TestCase):
    def setUp(self):
        self.car_rental_company = {
            "_id": "1",
            "type": "test_data/complex/CarRental",
            "name": "myCarRentalCompany",
            "cars": [
                {
                    "type": "test_data/complex/RentalCar",
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
        self.customer = {
            "_id": "4",
            "type": "test_data/complex/Customer",
            "name": "Jane",
            "car": {
                "address": "$1.cars[0]",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
        }
        self.engine = {
            "_id": "2",
            "type": "test_data/complex/EngineTest",
            "name": "myEngine",
            "description": "",
            "fuelPump": {
                "address": "$3",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
            "power": 120,
        }
        self.fuel_pump = {
            "_id": "3",
            "type": "test_data/complex/FuelPumpTest",
            "name": "fuelPump",
            "description": "A standard fuel pump",
        }
        self.document_repository = mock.Mock()
        self.document_repository.name = "datasource"
        self.document_repository.get = self.mock_get
        self.document_repository.find = self.mock_find
        self.document_service = get_mock_document_service(lambda x, y: self.document_repository)

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

    def test_attribute_no_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.cars[0].engine"), 0, resolve_references=False
            )
        )
        assert get_and_print_diff(root, self.car_rental_company["cars"][0]["engine"]) == []

    def test_attribute_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.cars[0].engine"), 0, resolve_references=True
            )
        )
        assert get_and_print_diff(root, self.engine) == []

    def test_query_no_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.customers(name=Jane)"), 0, resolve_references=False
            )
        )
        assert get_and_print_diff(root, self.car_rental_company["customers"][0]) == []

    def test_query_resolve(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.customers(name=Jane)"), 0, resolve_references=True
            )
        )
        assert get_and_print_diff(root, self.customer) == []

    def test_depth_0(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1"), 0, resolve_references=True)
        )
        assert get_and_print_diff(root, self.car_rental_company) == []

    def test_depth_1(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1"), 1, resolve_references=True)
        )
        assert get_and_print_diff(root, {**self.car_rental_company, "customers": [self.customer]}) == []

    def test_depth_2(self):
        root = tree_node_to_dict(
            self.document_service.get_document(Address.from_absolute("datasource/$1"), 2, resolve_references=True)
        )
        assert (
            get_and_print_diff(
                root,
                {
                    **self.car_rental_company,
                    "cars": [{**self.car_rental_company["cars"][0], "engine": self.engine}],
                    "customers": [{**self.customer, "car": self.car_rental_company["cars"][0]}],
                },
            )
            == []
        )

    def test_nested_depth_0(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.cars[0]"), 0, resolve_references=True
            )
        )
        assert get_and_print_diff(root, self.car_rental_company["cars"][0]) == []

    def test_nested_depth_1(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.cars[0]"), 1, resolve_references=True
            )
        )
        assert get_and_print_diff(root, {**self.car_rental_company["cars"][0], "engine": self.engine}) == []

    def test_nested_depth_2(self):
        root = tree_node_to_dict(
            self.document_service.get_document(
                Address.from_absolute("datasource/$1.cars[0]"), 2, resolve_references=True
            )
        )
        assert (
            get_and_print_diff(
                root, {**self.car_rental_company["cars"][0], "engine": {**self.engine, "fuelPump": self.fuel_pump}}
            )
            == []
        )
