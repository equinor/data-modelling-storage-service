import re
import unittest
from unittest import mock

import pytest

from common.exceptions import ApplicationException, NotFoundException
from common.reference import Reference
from common.utils.resolve_reference import resolve_reference
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_utils import get_mock_document_service


class ResolveReferenceTestCase(unittest.TestCase):
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
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Jon",
                    "car": {
                        "address": "^.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
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

    def test_id(self):
        ref = resolve_reference(Reference.fromabsolute("datasource/$1"), self.document_service.get_data_source)
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "1"
        assert ref.attribute_path == []
        assert ref.entity == self.car_rental_company

    def test_with_attributes(self):
        ref = resolve_reference(Reference.fromabsolute("datasource/$1.cars[0]"), self.document_service.get_data_source)
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "1"
        assert ref.attribute_path == ["cars", "[0]"]
        assert ref.entity == self.car_rental_company["cars"][0]

    def test_with_attributes_to_uncontained(self):
        ref = resolve_reference(
            Reference.fromabsolute("datasource/$1.cars[0].engine"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "1"
        assert ref.attribute_path == ["cars", "[0]", "engine"]
        assert ref.entity == self.car_rental_company["cars"][0]["engine"]

    def test_with_attributes_to_uncontained_child(self):
        ref = resolve_reference(
            Reference.fromabsolute("datasource/$1.cars[0].engine.fuelPump"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "2"
        assert ref.attribute_path == ["fuelPump"]
        assert ref.entity == self.engine["fuelPump"]

    def test_with_attributes_via_relative_ref(self):
        ref = resolve_reference(
            Reference.fromabsolute("datasource/$1.customers[1].car.engine"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "1"
        assert ref.attribute_path == ["cars", "[0]", "engine"]
        assert ref.entity == self.car_rental_company["cars"][0]["engine"]

    def test_with_query_to_uncontained(self):
        ref = resolve_reference(
            Reference.fromabsolute("datasource/$1.customers(name=Jane)"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "1"
        assert ref.attribute_path == ["customers", "[0]"]
        assert ref.entity == self.car_rental_company["customers"][0]

    def test_with_query_to_uncontained_child(self):
        ref = resolve_reference(
            Reference.fromabsolute("datasource/$1.customers(name=Jane).car"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "4"
        assert ref.attribute_path == ["car"]
        assert ref.entity == self.customer["car"]

    def test_invalid_id(self):
        with pytest.raises(
            NotFoundException, match=re.escape("No document with id '5' could be found in data source 'datasource'.")
        ):
            resolve_reference(Reference.fromabsolute("datasource/$5"), self.document_service.get_data_source)

    def test_invalid_query_no_document(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape("No document that match '_id=5' could be found in data source 'datasource'."),
        ):
            resolve_reference(Reference.fromabsolute("datasource/[(_id=5)]"), self.document_service.get_data_source)

    def test_invalid_query_no_attribute(self):
        with pytest.raises(ApplicationException, match=re.escape("No object matches filter 'name=Peter'")):
            resolve_reference(
                Reference.fromabsolute("datasource/$1.customers[(name=Peter)]"), self.document_service.get_data_source
            )

    def test_invalid_attribute(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(
                f"Invalid attribute 'cers'. Valid attributes are '{list(self.car_rental_company.keys())}'."
            ),
        ):
            resolve_reference(Reference.fromabsolute("datasource/$1.cers"), self.document_service.get_data_source)

    def test_invalid_index(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(f"Invalid index '[1]'. Valid indices are < {len(self.car_rental_company['cars'])}."),
        ):
            resolve_reference(Reference.fromabsolute("datasource/$1.cars[1]"), self.document_service.get_data_source)

    def test_invalid_reference_to_primitive(self):
        with pytest.raises(
            NotFoundException, match=re.escape("Path ['1', 'cars', '[0]', 'plateNumber'] leads to a primitive value.")
        ):
            resolve_reference(
                Reference.fromabsolute("datasource/$1.cars[0].plateNumber"), self.document_service.get_data_source
            )
