import unittest
from unittest import mock

from authentication.models import User
from common.utils.data_structure.compare import pretty_eq
from enums import SIMOS
from tests.unit.mock_utils import get_mock_document_service


class DocumentServiceTestCase(unittest.TestCase):
    def test_rename_attribute(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {"name": "some reference", "description": "", "type": "basic_blueprint"},
                "references": [],
            }
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return doc_storage["1"]
            return None

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider)
        document_service.rename_document(
            data_source_id="testing", parent_uid="1", document_id="1.nested", name="New_name"
        )

        actual = {"name": "New_name", "description": "", "type": "basic_blueprint"}

        assert pretty_eq(actual, doc_storage["1"]["nested"]) is None

    def test_rename_root_package(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "RootPackage",
                "description": "My root package",
                "type": SIMOS.PACKAGE.value,
                "isRoot": True,
                "content": [],
            }
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return doc_storage["1"].copy()
            return None

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider)
        document_service.rename_document(data_source_id="testing", document_id="1", name="New_name")

        actual = {"_id": "1", "name": "New_name"}

        assert pretty_eq(actual, doc_storage["1"]) is None

    def test_rename_single_reference(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "references": [],
                "reference": {"ref": "2", "name": "Reference", "type": SIMOS.LINK},
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider)
        document_service.rename_document(data_source_id="testing", document_id="2", parent_uid="1", name="New_name")

        actual = {"_id": "1", "reference": {"_id": "2", "name": "New_name", "type": "basic_blueprint"}}
        actual2 = {"_id": "2", "name": "New_name", "type": "basic_blueprint"}

        assert pretty_eq(actual, doc_storage["1"]) is None
        assert pretty_eq(actual2, doc_storage["2"]) is None

    def test_rename_reference_list(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "all_contained_cases_blueprint",
                "nested": {"name": "Nested", "description": "", "type": "basic_blueprint"},
                "reference": {
                    "ref": "2",
                    "targetName": "Reference",
                    "targetType": "basic_blueprint",
                    "type": SIMOS.STORAGE_ADDRESS.value,
                },
                "references": [
                    {
                        "ref": "2",
                        "targetName": "Reference",
                        "targetType": "basic_blueprint",
                        "type": SIMOS.STORAGE_ADDRESS.value,
                    }
                ],
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "basic_blueprint"},
        }

        def mock_get(document_id: str):
            return doc_storage[document_id]

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = get_mock_document_service(repository_provider)
        document_service.rename_document(data_source_id="testing", document_id="2", parent_uid="1", name="New_name")

        actual = {
            "_id": "1",
            "references": [
                {
                    "ref": "2",
                    "targetName": "New_name",
                    "targetType": "basic_blueprint",
                    "type": SIMOS.STORAGE_ADDRESS.value,
                }
            ],
        }
        actual2 = {"_id": "2", "name": "New_name", "type": "basic_blueprint"}

        assert pretty_eq(actual, doc_storage["1"]) is None
        assert pretty_eq(actual2, doc_storage["2"]) is None
