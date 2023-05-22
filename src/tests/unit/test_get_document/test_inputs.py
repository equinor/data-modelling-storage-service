import re
import unittest
from unittest import mock

import pytest

from common.exceptions import ApplicationException, NotFoundException
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
                    "type": "test_data/complex/Customer",
                    "name": "Jane",
                    "car": {
                        "address": "$1.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                }
            ],
        }
        self.engine = {
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
        return None

    def mock_find(self, query: dict) -> list[dict]:
        documents: list[dict] = [self.car_rental_company, self.engine, self.fuel_pump]
        for key, value in query.items():
            documents = list(filter(lambda x: key in x and x[key] == value, documents))
        return documents

    def test_invalid_id(self):
        with pytest.raises(
            NotFoundException, match=re.escape("No document with id '4' could be found in data source 'datasource'.")
        ):
            self.document_service.get_document("datasource/$4")

    def test_invalid_query_no_document(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape("No document that match '_id=4' could be found in data source 'datasource'."),
        ):
            self.document_service.get_document("datasource/[(_id=4)]")

    def test_invalid_query_no_attribute(self):
        with pytest.raises(ApplicationException, match=re.escape("No object matches filter 'name=Peter'")):
            self.document_service.get_document("datasource/$1.customers[(name=Peter)]")

    def test_invalid_attribute(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(
                f"Invalid attribute 'cers'. Valid attributes are '{list(self.car_rental_company.keys())}'."
            ),
        ):
            self.document_service.get_document("datasource/$1.cers")

    def test_invalid_index(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(f"Invalid index '[1]'. Valid indices are < {len(self.car_rental_company['cars'])}."),
        ):
            self.document_service.get_document("datasource/$1.cars[1]")

    def test_invalid_reference_to_primitive(self):
        with pytest.raises(
            NotFoundException, match=re.escape(f"Path ['1', 'cars', '[0]', 'plateNumber'] leads to a primitive value.")
        ):
            self.document_service.get_document("datasource/$1.cars[0].plateNumber")

    def test_depth_0(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1", 0, resolve_links=True))
        assert get_and_print_diff(root, self.car_rental_company) == []

    def test_depth_1(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1", 1, resolve_links=True))
        assert get_and_print_diff(root, self.car_rental_company) == []

    def test_depth_2(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1", 2, resolve_links=True))
        assert (
            get_and_print_diff(
                root,
                {
                    **self.car_rental_company,
                    "cars": [{**self.car_rental_company["cars"][0], "engine": self.engine}],
                    "customers": [
                        {**self.car_rental_company["customers"][0], "car": self.car_rental_company["cars"][0]},
                    ],
                },
            )
            == []
        )

    def test_nested_depth_0(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1.cars[0]", 0, resolve_links=True))
        assert get_and_print_diff(root, self.car_rental_company["cars"][0]) == []

    def test_nested_depth_1(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1.cars[0]", 1, resolve_links=True))
        assert get_and_print_diff(root, {**self.car_rental_company["cars"][0], "engine": self.engine}) == []

    def test_nested_depth_2(self):
        root = tree_node_to_dict(self.document_service.get_document("datasource/$1.cars[0]", 2, resolve_links=True))
        assert (
            get_and_print_diff(
                root, {**self.car_rental_company["cars"][0], "engine": {**self.engine, "fuelPump": self.fuel_pump}}
            )
            == []
        )
