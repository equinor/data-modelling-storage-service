from pydantic import conint

from authentication.models import User
from common.address import Address
from services.document_service.document_service import DocumentService
from storage.internal.get_data_source_cached import get_data_source_cached


def get_document_use_case(
    user: User,
    address: str,
    depth: conint(gt=-1, lt=1000),  # type: ignore
    repository_provider=get_data_source_cached,
):
    """Get document by reference."""
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    resolved_document, _ = document_service.resolve_document(Address.from_absolute(address), depth)
    return resolved_document
