import unittest
from unittest import mock

import pytest

from common.tree_node_serializer import tree_node_to_dict
from common.utils.data_structure.compare import pretty_eq
from enums import SIMOS, Protocols
from tests.unit.mock_utils import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def test_references_that_uses_wrong_protocol(self):
        my_car_rental = {
            "_id": "1",
            "type": "test_data/complex/CarRental",
            "name": "myCarRental",
            "description": "",
            "extends": [SIMOS.NAMED_ENTITY.value],
            "cars": [{"type": "test_data/complex/CarTest", "name": "Volvo 240"}],
            "customers": [
                {
                    "type": "test_data/complex/Customer",
                    "name": "Wrong protocol",
                    "car": {
                        "ref": "wrong:///1.cars.0",
                        "targetName": "Volvo 240",
                        "targetType": "test_data/complex/CarTest",
                        "type": SIMOS.LINK.value,
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
                        {
                            "ref": "1",
                            "targetName": "myCarRental",
                            "targetType": "test_data/complex/CarRental",
                            "type": SIMOS.LINK.value,
                        },
                    ]
                }
            ]

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.find = mock_find

        document_service = get_mock_document_service(lambda x, y: document_repository)
        with pytest.raises(Exception, match=r"The protocol 'wrong' is not supported"):
            tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

    def test_references_that_point_to_nested_attribute(self):
        my_car_rental = {
            "_id": "1",
            "type": "test_data/complex/CarRental",
            "name": "myCarRental",
            "description": "",
            "extends": [SIMOS.NAMED_ENTITY.value],
            "cars": [{"type": "test_data/complex/CarTest", "name": "Volvo 240"}],
            "customers": [
                {
                    "type": "test_data/complex/Customer",
                    "name": "Root reference by id",
                    "car": {
                        "ref": f"{Protocols.DMSS.value}:///1.cars.0",
                        "targetName": "Volvo 240",
                        "targetType": "test_data/complex/CarTest",
                        "type": SIMOS.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Root reference by path",
                    "car": {
                        "ref": f"{Protocols.DMSS.value}:///complex/myCarRental.cars.0",
                        "targetName": "Volvo 240",
                        "targetType": "test_data/complex/CarTest",
                        "type": SIMOS.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Absolute reference by id",
                    "car": {
                        "ref": f"{Protocols.DMSS.value}://test_data/1.cars.0",
                        "targetName": "Volvo 240",
                        "targetType": "test_data/complex/CarTest",
                        "type": SIMOS.LINK.value,
                    },
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Absolute reference by path",
                    "car": {
                        "ref": f"{Protocols.DMSS.value}://test_data/complex/myCarRental.cars.0",
                        "targetName": "Volvo 240",
                        "targetType": "test_data/complex/CarTest",
                        "type": SIMOS.LINK.value,
                    },
                },
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
                        {
                            "ref": "1",
                            "targetName": "myCarRental",
                            "targetType": "test_data/complex/CarRental",
                            "type": SIMOS.LINK.value,
                        },
                    ]
                }
            ]

        document_repository = mock.Mock()
        document_repository.get = mock_get
        document_repository.find = mock_find

        document_service = get_mock_document_service(lambda x, y: document_repository)
        root = tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

        assert isinstance(root, dict)

        actual = {
            "_id": "1",
            "type": "test_data/complex/CarRental",
            "name": "myCarRental",
            "cars": [{"type": "test_data/complex/CarTest", "name": "Volvo 240"}],
            "customers": [
                {
                    "type": "test_data/complex/Customer",
                    "name": "Root reference by id",
                    "car": {"type": "test_data/complex/CarTest", "name": "Volvo 240"},
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Root reference by path",
                    "car": {"type": "test_data/complex/CarTest", "name": "Volvo 240"},
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Absolute reference by id",
                    "car": {"type": "test_data/complex/CarTest", "name": "Volvo 240"},
                },
                {
                    "type": "test_data/complex/Customer",
                    "name": "Absolute reference by path",
                    "car": {"type": "test_data/complex/CarTest", "name": "Volvo 240"},
                },
            ],
        }

        assert pretty_eq(actual, root) is None

    def test_get_complete_document(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            "reference": {
                "ref": "2",
                "targetName": "Reference",
                "targetType": "basic_blueprint",
                "type": SIMOS.LINK.value,
            },
            "references": [
                {"ref": "3", "targetName": "Reference1", "targetType": "basic_blueprint", "type": SIMOS.LINK.value},
                {"ref": "4", "targetName": "Reference2", "targetType": "basic_blueprint", "type": SIMOS.LINK.value},
            ],
        }

        document_2 = {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"}
        document_3 = {"_id": "3", "name": "Reference1", "description": "", "type": "basic_blueprint"}
        document_4 = {"_id": "4", "name": "Reference2", "description": "", "type": "basic_blueprint"}

        def mock_get(document_id: str):
            if document_id == "1":
                return document_1.copy()
            if document_id == "2":
                return document_2.copy()
            if document_id == "3":
                return document_3.copy()
            if document_id == "4":
                return document_4.copy()
            return None

        document_repository = mock.Mock()
        document_repository.get = mock_get

        document_service = get_mock_document_service(lambda x, y: document_repository)
        root = tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

        assert isinstance(root, dict)

        actual = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
            "reference": document_2,
            "references": [document_3, document_4],
        }

        assert pretty_eq(actual, root) is None

    def test_get_complete_nested_reference(self):
        document_1 = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_second_level_reference",
            "contained_with_child_references": {
                "name": "First child",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {
                    "ref": "2",
                    "targetName": "Reference",
                    "targetType": "basic_blueprint",
                    "type": SIMOS.LINK.value,
                },
                "references": [
                    {
                        "ref": "3",
                        "targetName": "Reference1",
                        "targetType": "basic_blueprint",
                        "type": SIMOS.LINK.value,
                    },
                    {
                        "ref": "4",
                        "targetName": "Reference2",
                        "targetType": "basic_blueprint",
                        "type": SIMOS.LINK.value,
                    },
                ],
            },
        }

        document_2 = {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"}
        document_3 = {"_id": "3", "name": "Reference1", "description": "", "type": "basic_blueprint"}
        document_4 = {"_id": "4", "name": "Reference2", "description": "", "type": "basic_blueprint"}

        def mock_get(document_id: str):
            if document_id == "1":
                return document_1.copy()
            if document_id == "2":
                return document_2.copy()
            if document_id == "3":
                return document_3.copy()
            if document_id == "4":
                return document_4.copy()
            return None

        document_repository = mock.Mock()
        document_repository.get = mock_get

        document_service = get_mock_document_service(lambda x, y: document_repository)
        root = tree_node_to_dict(document_service.get_node_by_uid("datasource", "1"))

        assert isinstance(root, dict)

        actual = {
            "_id": "1",
            "name": "Parent",
            "description": "",
            "type": "blueprint_with_second_level_reference",
            "contained_with_child_references": {
                "name": "First child",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": document_2,
                "references": [document_3, document_4],
            },
        }

        assert pretty_eq(actual, root) is None
