import unittest
from unittest import mock

from domain_classes.user import User

from domain_classes.dto import DTO
from services.document_service import DocumentService
from enums import DMT
from tests.unit.mock_blueprint_provider import blueprint_provider
from utils.data_structure.compare import pretty_eq


class DocumentServiceTestCase(unittest.TestCase):
    def test_rename_attribute(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
                "reference": {"name": "some reference", "description": "", "type": "blueprint_2"},
                "references": [],
            }
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return DTO(data=doc_storage["1"])
            return None

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.rename_document(
            data_source_id="testing", parent_uid="1", document_id="1.nested", name="New_name"
        )

        actual = {"name": "New_name", "description": "", "type": "blueprint_2"}

        assert pretty_eq(actual, doc_storage["1"]["nested"]) is None

    def test_rename_root_package(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "RootPackage",
                "description": "My root package",
                "type": DMT.PACKAGE.value,
                "isRoot": True,
                "content": [],
            }
        }

        def mock_get(document_id: str):
            if document_id == "1":
                return DTO(data=doc_storage["1"].copy())
            return None

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
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
                "type": "blueprint_1",
                "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
                "references": [],
                "reference": {"_id": "2", "name": "Reference", "type": "blueprint_2"},
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.rename_document(data_source_id="testing", document_id="2", parent_uid="1", name="New_name")

        actual = {"_id": "1", "reference": {"_id": "2", "name": "New_name", "type": "blueprint_2"}}
        actual2 = {"_id": "2", "name": "New_name", "type": "blueprint_2"}

        assert pretty_eq(actual, doc_storage["1"]) is None
        assert pretty_eq(actual2, doc_storage["2"]) is None

    def test_rename_reference_list(self):
        document_repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "Parent",
                "description": "",
                "type": "blueprint_1",
                "nested": {"name": "Nested", "description": "", "type": "blueprint_2"},
                "reference": {"_id": "2", "name": "Reference", "type": "blueprint_2"},
                "references": [{"_id": "2", "name": "Reference", "type": "blueprint_2"}],
            },
            "2": {"_id": "2", "name": "Reference", "description": "", "type": "blueprint_2"},
        }

        def mock_get(document_id: str):
            return DTO(doc_storage[document_id])

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        document_repository.get = mock_get
        document_repository.update = mock_update

        def repository_provider(data_source_id, user: User):
            if data_source_id == "testing":
                return document_repository

        document_service = DocumentService(
            repository_provider=repository_provider, blueprint_provider=blueprint_provider
        )
        document_service.rename_document(data_source_id="testing", document_id="2", parent_uid="1", name="New_name")

        actual = {"_id": "1", "references": [{"_id": "2", "name": "New_name", "type": "blueprint_2"}]}
        actual2 = {"_id": "2", "name": "New_name", "type": "blueprint_2"}

        assert pretty_eq(actual, doc_storage["1"]) is None
        assert pretty_eq(actual2, doc_storage["2"]) is None
