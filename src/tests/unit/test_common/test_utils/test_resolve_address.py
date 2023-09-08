import re
import unittest
from unittest import mock

import pytest

from common.address import Address
from common.exceptions import ApplicationException, NotFoundException
from common.utils.resolve_address import resolve_address
from enums import REFERENCE_TYPES, SIMOS
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class ResolveReferenceTestCase(unittest.TestCase):
    def setUp(self):
        self.car_rental_company = {
            "_id": "car_rental_company_id",
            "type": "CarRental",
            "name": "myCarRentalCompany",
            "cars": [
                {
                    "type": "RentalCar",
                    "name": "Volvo 240",
                    "plateNumber": "123",
                    "engine": {
                        "address": "$engine_id",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                }
            ],
            "customers": [
                {
                    "address": "$customer_id",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
                {
                    "type": "Customer",
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
            "_id": "customer_id",
            "type": "Customer",
            "name": "Jane",
            "car": {
                "address": "$car_rental_company_id.cars[0]",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
        }
        self.engine = {
            "_id": "engine_id",
            "type": "EngineTest",
            "name": "myEngine",
            "description": "",
            "fuelPump": {
                "address": "$fuel_pump_id",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            },
            "power": 120,
        }
        self.fuel_pump = {
            "_id": "fuel_pump_id",
            "type": "FuelPumpTest",
            "name": "fuelPump",
            "description": "A standard fuel pump",
        }
        self.document_repository = mock.Mock()
        self.document_repository.name = "datasource"
        self.document_repository.get = self.mock_get
        self.document_repository.find = self.mock_find
        self.document_service = get_mock_document_service(lambda x, y: self.document_repository)

    def mock_get(self, document_id: str):
        if document_id == "car_rental_company_id":
            return {**self.car_rental_company}
        if document_id == "engine_id":
            return {**self.engine}
        if document_id == "fuel_pump_id":
            return {**self.fuel_pump}
        if document_id == "customer_id":
            return {**self.customer}
        return None

    def mock_find(self, query: dict) -> list[dict]:
        documents: list[dict] = [self.car_rental_company, self.engine, self.fuel_pump, self.customer]
        for key, value in query.items():
            documents = list(filter(lambda x: key in x and x[key] == value, documents))
        return documents

    def test_id(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "car_rental_company_id"
        assert ref.attribute_path == []
        assert ref.entity == self.car_rental_company

    def test_with_attributes(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.cars[0]"), self.document_service.get_data_source
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "car_rental_company_id"
        assert ref.attribute_path == ["cars", "[0]"]
        assert ref.entity == self.car_rental_company["cars"][0]

    def test_with_attributes_to_uncontained(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.cars[0].engine"),
            self.document_service.get_data_source,
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "car_rental_company_id"
        assert ref.attribute_path == ["cars", "[0]", "engine"]
        assert ref.entity == self.car_rental_company["cars"][0]["engine"]

    def test_with_attributes_to_uncontained_child(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.cars[0].engine.fuelPump"),
            self.document_service.get_data_source,
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "engine_id"
        assert ref.attribute_path == ["fuelPump"]
        assert ref.entity == self.engine["fuelPump"]

    def test_with_attributes_via_relative_ref(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.customers[1].car.engine"),
            self.document_service.get_data_source,
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "car_rental_company_id"
        assert ref.attribute_path == ["cars", "[0]", "engine"]
        assert ref.entity == self.car_rental_company["cars"][0]["engine"]

    def test_with_query_to_uncontained(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.customers(name=Jane)"),
            self.document_service.get_data_source,
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "car_rental_company_id"
        assert ref.attribute_path == ["customers", "[0]"]
        assert ref.entity == self.car_rental_company["customers"][0]

    def test_with_query_to_uncontained_child(self):
        ref = resolve_address(
            Address.from_absolute("datasource/$car_rental_company_id.customers(name=Jane).car"),
            self.document_service.get_data_source,
        )
        assert ref.data_source_id == "datasource"
        assert ref.document_id == "customer_id"
        assert ref.attribute_path == ["car"]
        assert ref.entity == self.customer["car"]

    def test_invalid_id(self):
        with pytest.raises(
            NotFoundException, match=re.escape("No document with id 'x' could be found in data source 'datasource'.")
        ):
            resolve_address(Address.from_absolute("datasource/$x"), self.document_service.get_data_source)

    def test_invalid_query_no_document(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape("No document that match '_id=xxx' could be found in data source 'datasource'."),
        ):
            resolve_address(Address.from_absolute("datasource/[(_id=xxx)]"), self.document_service.get_data_source)

    def test_invalid_query_no_attribute(self):
        with pytest.raises(ApplicationException, match=re.escape("No object matches filter 'name=Peter'")):
            resolve_address(
                Address.from_absolute("datasource/$car_rental_company_id.customers[(name=Peter)]"),
                self.document_service.get_data_source,
            )

    def test_invalid_attribute(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(
                f"Invalid attribute 'xxx'. Valid attributes are '{list(self.car_rental_company.keys())}'."
            ),
        ):
            resolve_address(
                Address.from_absolute("datasource/$car_rental_company_id.xxx"), self.document_service.get_data_source
            )

    def test_invalid_index(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(f"Invalid index '[1]'. Valid indices are < {len(self.car_rental_company['cars'])}."),
        ):
            resolve_address(
                Address.from_absolute("datasource/$car_rental_company_id.cars[1]"),
                self.document_service.get_data_source,
            )

    def test_invalid_reference_to_primitive(self):
        with pytest.raises(
            NotFoundException,
            match=re.escape(
                "Path ['car_rental_company_id', 'cars', '[0]', 'plateNumber'] leads to a primitive value."
            ),
        ):
            resolve_address(
                Address.from_absolute("datasource/$car_rental_company_id.cars[0].plateNumber"),
                self.document_service.get_data_source,
            )
