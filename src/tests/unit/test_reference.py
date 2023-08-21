import unittest
from copy import deepcopy
from unittest import mock

from common.address import Address
from common.exceptions import ValidationException
from enums import REFERENCE_TYPES, SIMOS
from features.document.use_cases.add_document_use_case import add_document_use_case
from tests.unit.mock_utils import get_mock_document_service


class ReferenceTestCase(unittest.TestCase):
    def test_insert_reference(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {
                    "address": "$123123123",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
            "2d7c3249-985d-43d2-83cf-a887e440825a": {
                "_id": "2d7c3249-985d-43d2-83cf-a887e440825a",
                "name": "something",
                "description": "",
                "type": "basic_blueprint",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = lambda x: doc_storage[str(x)]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)
        reference = {
            "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }
        document_service.update_document(
            Address("$1.uncontained_in_every_way", "testing"), reference, update_uncontained=False
        )
        assert doc_storage["1"]["uncontained_in_every_way"] == reference

    def test_insert_reference_too_many_attributes(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {
                    "address": "$123123123",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            },
            "2d7c3249-985d-43d2-83cf-a887e440825a": {
                "_id": "2d7c3249-985d-43d2-83cf-a887e440825a",
                "name": "something",
                "description": "",
                "type": "basic_blueprint",
            },
        }

        def mock_get(document_id: str):
            return doc_storage[str(document_id)]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        reference_entity = {
            "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
            "description": "hallO",
            "something": "something",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

        with self.assertRaises(ValidationException):
            document_service.update_document(Address("$1.uncontained_in_every_way", "testing"), reference_entity)

    def test_insert_reference_missing_required_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {
                    "address": "$123123123",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                },
            }
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        reference_entity_with_missing_attribute = {"address": "$123", "type": SIMOS.REFERENCE.value}
        with self.assertRaises(ValidationException):
            document_service.update_document(
                Address("$1.uncontained_in_every_way", "testing"), reference_entity_with_missing_attribute
            )

    # TODO if the attribute to remove is required, document_service.remove() should give an error.
    # This test must be updated such that document_service.remove() tries to remove an optional attribute instead.
    def test_remove_reference(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {
                    "_id": "something",
                    "name": "something",
                    "description": "",
                    "type": "basic_blueprint",
                },
            },
            "something": {
                "_id": "something",
                "name": "something",
                "description": "",
                "type": "basic_blueprint",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = lambda id: doc_storage[id]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        document_service.remove(Address("$1.uncontained_in_every_way", "testing"))
        assert "uncontained_in_every_way" not in doc_storage["1"]

    def test_remove_nested_reference(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_with_second_level_nested_uncontained_attribute",
                "i_have_a_uncontained_attribute": {
                    "name": "something",
                    "description": "",
                    "type": "uncontained_blueprint",
                    "uncontained_in_every_way": {
                        "_id": "something",
                        "name": "something",
                        "description": "",
                        "type": "basic_blueprint",
                    },
                },
            },
            "something": {
                "_id": "something",
                "name": "something",
                "description": "",
                "type": "basic_blueprint",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = lambda id: doc_storage[id]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        document_service.remove(Address("$1.i_have_a_uncontained_attribute.uncontained_in_every_way", "testing"))
        assert "uncontained_in_every_way" not in doc_storage["1"]["i_have_a_uncontained_attribute"]

    def test_remove_reference_in_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_list_blueprint",
                "uncontained_in_every_way": [
                    {
                        "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                    {
                        "address": "$42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    },
                ],
            },
            "2d7c3249-985d-43d2-83cf-a887e440825a": {
                "_id": "2d7c3249-985d-43d2-83cf-a887e440825a",
                "name": "something",
                "type": "basic_blueprint",
            },
            "42dbe4a5-0eb0-4ee2-826c-695172c3c35a": {
                "_id": "42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
                "name": "something",
                "type": "basic_blueprint",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda x: doc_storage[str(x)]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        document_service.remove(Address("$1.uncontained_in_every_way[0]", "testing"))
        assert len(doc_storage["1"]["uncontained_in_every_way"]) == 1
        assert doc_storage["1"]["uncontained_in_every_way"][0] == {
            "address": "$42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

    def test_add_reference_in_list(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_list_blueprint",
                "uncontained_in_every_way": [
                    {
                        "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    }
                ],
            },
            "2d7c3249-985d-43d2-83cf-a887e440825a": {
                "_id": "2d7c3249-985d-43d2-83cf-a887e440825a",
                "name": "something",
                "type": "basic_blueprint",
            },
            "42dbe4a5-0eb0-4ee2-826c-695172c3c35a": {
                "_id": "42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
                "name": "something",
                "type": "basic_blueprint",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda x: doc_storage[str(x)]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)
        reference = {
            "address": "$42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }
        add_document_use_case(
            address=Address("$1.uncontained_in_every_way", "testing"),
            document=reference,
            update_uncontained=True,
            document_service=document_service,
        )
        assert len(doc_storage["1"]["uncontained_in_every_way"]) == 2
        assert doc_storage["1"]["uncontained_in_every_way"][1] == reference
