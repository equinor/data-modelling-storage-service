import unittest
from copy import deepcopy
from unittest import mock

import pytest

from common.address import Address
from common.tree_node_serializer import tree_node_to_dict
from common.utils.data_structure.compare import get_and_print_diff
from common.utils.data_structure.has_key_value_pairs import has_key_value_pairs
from enums import REFERENCE_TYPES, SIMOS, Protocols
from tests.unit.mock_utils import get_mock_document_service


class GetDocumentResolveTestCase(unittest.TestCase):
    def test_references_that_uses_wrong_protocol(self):
        my_car_rental = {
            "_id": "1",
            "type": "test_data/complex/CarRental",
            "name": "myCarRental",
            "cars": [
                {"type": "test_data/complex/RentalCar", "name": "Volvo 240", "plateNumber": "123"},
                {"type": "test_data/complex/RentalCar", "name": "Ferrari", "plateNumber": "456"},
            ],
            "customers": [
                {
                    "type": "test_data/complex/Customer",
                    "name": "Wrong protocol",
                    "car": {
                        "address": "wrong://$1.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                }
            ],
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return my_car_rental.copy()
            return None

        def mock_find(target: dict):
            # Used when resolving reference using paths.
            return [
                {
                    "content": [
                        {"address": "$1", "type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value},
                    ]
                }
            ]

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.find = mock_find

        document_service = get_mock_document_service(lambda x, y: document_repository)
        with pytest.raises(Exception, match=r"The protocol 'wrong' is not supported"):
            tree_node_to_dict(
                document_service.get_document(Address.from_absolute("datasource/$1"), resolve_links=True, depth=9)
            )

    def test_references(self):
        my_car_rental = {
            "_id": "2",
            "type": "test_data/complex/CarRental",
            "name": "myCarRental",
            "cars": [
                {
                    "type": "test_data/complex/RentalCar",
                    "name": "Volvo 240",
                    "plateNumber": "123",
                    "engine": {
                        "address": f"{Protocols.DMSS.value}://another_data_source/$3",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/RentalCar",
                    "name": "Ferrari",
                    "plateNumber": "456",
                    "engine": {
                        "address": f"{Protocols.DMSS.value}://another_data_source/parts/engines/myEngine",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            ],
            "customers": [
                {
                    "type": "test_data/complex/Customer",
                    "name": "Full absolute path prefixed with protocol",
                    "car": {
                        "address": f"{Protocols.DMSS.value}://test_data/complex/myCarRental.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the destination data source by id",
                    "car": {
                        "address": f"/$2.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the destination data source by path",
                    "car": {
                        "address": f"/complex/myCarRental.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the destination data source by query",
                    "car": {
                        "address": f"/[(_id=1)].content[(name=myCarRental)].cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the destination data source by query on array",
                    "car": {
                        "address": f"/[(_id=1)].content[(name=myCarRental)].cars[(name=Volvo 240)]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Test",
                    "car": {
                        "address": f"/complex.content[(name=myCarRental)].cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Test2",
                    "car": {
                        "address": f"/complex.content[0].cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the document",
                    "car": {
                        "address": f"^.cars[0]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Relative from the document with query on plate number",
                    "car": {
                        "address": f"^.cars[(plateNumber=456,name=Ferrari)]",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                },
            ],
        }

        test_data_data_source = [
            {
                "_id": "1",
                "name": "complex",
                "isRoot": True,
                "type": SIMOS.PACKAGE.value,
                "content": [
                    {"address": "$2", "type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value},
                ],
            }
        ]

        def mock_get_inside_test_data(document_id: str):
            if document_id == "1":
                return deepcopy(test_data_data_source[0])
            if document_id == "2":
                return deepcopy(my_car_rental)
            return None

        my_engine = {
            "_id": "3",
            "name": "myEngine",
            "description": "Some description",
            "fuelPump": {
                "name": "fuelPump",
                "description": "A standard fuel pump",
                "type": "test_data/complex/FuelPumpTest",
            },
            "power": 120,
            "type": "test_data/complex/EngineTest",
        }

        engines = {
            "_id": "2",
            "name": "engines",
            "isRoot": True,
            "content": [
                {"address": "$3", "type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value},
            ],
        }

        another_data_source = [
            {
                "_id": "1",
                "name": "parts",
                "isRoot": True,
                "content": [
                    {"address": "$2", "type": SIMOS.REFERENCE.value, "referenceType": REFERENCE_TYPES.LINK.value},
                ],
            },
            my_engine,
        ]

        def mock_get_inside_another_data_source(document_id: str):
            if document_id == "1":
                return deepcopy(another_data_source[0])
            if document_id == "2":
                return deepcopy(engines)
            if document_id == "3":
                return deepcopy(my_engine)
            return None

        def find(target: dict, data_source: list) -> dict:
            """Utility method to be able to search for a document inside a test data source."""
            hit = next((f for f in data_source if has_key_value_pairs(f, target)), None)
            if hit:
                return [deepcopy(hit)]

        def mock_data_source(data_source_id: str, user: dict):
            document_repository = mock.Mock()
            document_repository.name = data_source_id
            if data_source_id == "test_data":
                document_repository.get = mock_get_inside_test_data
                document_repository.find = lambda target: find(target, test_data_data_source)
            if data_source_id == "another_data_source":
                document_repository.get = mock_get_inside_another_data_source
                document_repository.find = lambda target: find(target, another_data_source)
            return document_repository

        document_service = get_mock_document_service(mock_data_source)
        actual = tree_node_to_dict(
            document_service.get_document(Address.from_absolute("test_data/$2"), resolve_links=True, depth=99)
        )
        complex_package = tree_node_to_dict(
            document_service.get_document(Address.from_absolute("test_data/$1"), resolve_links=True, depth=99)
        )

        assert isinstance(actual, dict)

        expected_engine = {**my_engine}
        expected_volvo = {**my_car_rental["cars"][0], "engine": expected_engine}
        expected_ferrari = {**my_car_rental["cars"][1], "engine": expected_engine}
        expected_customers = [
            {**my_car_rental["customers"][0], "car": expected_volvo},
            {**my_car_rental["customers"][1], "car": expected_volvo},
            {**my_car_rental["customers"][2], "car": expected_volvo},
            {**my_car_rental["customers"][3], "car": expected_volvo},
            {**my_car_rental["customers"][4], "car": expected_volvo},
            {**my_car_rental["customers"][5], "car": expected_volvo},
            {**my_car_rental["customers"][6], "car": expected_volvo},
            {**my_car_rental["customers"][7], "car": expected_volvo},
            {**my_car_rental["customers"][8], "car": expected_ferrari},
        ]
        expected = {**my_car_rental, "cars": [expected_volvo, expected_ferrari], "customers": expected_customers}

        assert get_and_print_diff(actual, expected) == []
        assert get_and_print_diff(complex_package["content"][0], expected) == []
