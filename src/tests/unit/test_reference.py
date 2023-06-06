import unittest
from unittest import mock

from pydantic import ValidationError

from common.exceptions import BadRequestException, NotFoundException
from enums import REFERENCE_TYPES, SIMOS
from restful.request_types.shared import ReferenceEntity
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
                "uncontained_in_every_way": {},
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
        reference = ReferenceEntity.parse_obj(
            {
                "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                "type": SIMOS.REFERENCE.value,
                "referenceType": REFERENCE_TYPES.LINK.value,
            }
        )
        document_service.insert_reference(
            "testing",
            document_id="$1",
            reference=reference,
            attribute_path="uncontained_in_every_way",
        )
        assert doc_storage["1"]["uncontained_in_every_way"] == {
            "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

    def test_insert_reference_target_does_not_exist(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {},
            }
        }

        def mock_get(document_id: str):
            try:
                return doc_storage[str(document_id)]
            except KeyError:
                raise NotFoundException(f"{document_id} was not found in the 'test' data-sources lookupTable")

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        with self.assertRaises(NotFoundException):
            document_service.insert_reference(
                "testing",
                document_id="$1",
                reference=ReferenceEntity.parse_obj(
                    {
                        "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    }
                ),
                attribute_path="uncontained_in_every_way",
            )

    def test_insert_reference_target_exists_but_wrong_type(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {},
            },
            "2d7c3249-985d-43d2-83cf-a887e440825a": {
                "_id": "2d7c3249-985d-43d2-83cf-a887e440825a",
                "name": "something",
                "description": "hgallo",
                "type": "ExtendedBlueprint",
                "another_value": "hei du",
            },
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda x: doc_storage[str(x)]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        with self.assertRaises(BadRequestException):
            document_service.insert_reference(
                "testing",
                document_id="$1",
                reference=ReferenceEntity.parse_obj(
                    {
                        "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                        "type": SIMOS.REFERENCE.value,
                        "referenceType": REFERENCE_TYPES.LINK.value,
                    }
                ),
                attribute_path="uncontained_in_every_way",
            )

    def test_insert_reference_too_many_attributes(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {},
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

        document_service.insert_reference(
            "testing",
            document_id="$1",
            reference=ReferenceEntity.parse_obj(
                {
                    "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
                    "description": "hallO",
                    "something": "something",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                }
            ),
            attribute_path="uncontained_in_every_way",
        )
        assert doc_storage["1"]["uncontained_in_every_way"] == {
            "address": "$2d7c3249-985d-43d2-83cf-a887e440825a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }

    def test_insert_reference_missing_required_attribute(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "uncontained_blueprint",
                "uncontained_in_every_way": {},
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

        with self.assertRaises(ValidationError):
            document_service.insert_reference(
                "testing",
                document_id="1",
                reference=ReferenceEntity.parse_obj({"_id": "something", "type": "something"}),
                attribute_path="uncontained_in_every_way",
            )

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

        document_service.remove_reference(
            "testing",
            document_id="$1",
            attribute_path="uncontained_in_every_way",
        )
        assert doc_storage["1"]["uncontained_in_every_way"] == {}

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

        document_service.remove_reference(
            "testing",
            document_id="$1",
            attribute_path="i_have_a_uncontained_attribute.uncontained_in_every_way",
        )
        assert doc_storage["1"]["i_have_a_uncontained_attribute"]["uncontained_in_every_way"] == {}

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

        document_service.remove_reference(
            "testing",
            document_id="$1",
            attribute_path="uncontained_in_every_way.0",
        )
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
        document_service.insert_reference(
            "testing",
            document_id="$1",
            reference=ReferenceEntity(
                **{
                    "address": "$42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
                    "type": SIMOS.REFERENCE.value,
                    "referenceType": REFERENCE_TYPES.LINK.value,
                }
            ),
            attribute_path="uncontained_in_every_way",
        )
        assert len(doc_storage["1"]["uncontained_in_every_way"]) == 2
        assert doc_storage["1"]["uncontained_in_every_way"][1] == {
            "address": "$42dbe4a5-0eb0-4ee2-826c-695172c3c35a",
            "type": SIMOS.REFERENCE.value,
            "referenceType": REFERENCE_TYPES.LINK.value,
        }
