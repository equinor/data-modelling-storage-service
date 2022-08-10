from enums import SIMOS

from authentication.models import User
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from common.utils.string_helpers import split_absolute_ref


def add_file_use_case(
    user: User, absolute_ref: str, data: dict, update_uncontained: bool, repository_provider=get_data_source
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document = document_service.add_document(
        absolute_ref=absolute_ref, data=data, update_uncontained=update_uncontained
    )
    # Do not invalidate the blueprint cache if it was not a blueprint that was changed
    if data["type"] == SIMOS.BLUEPRINT.value:
        document_service.invalidate_cache()

    data_source, _, _ = split_absolute_ref(absolute_ref)
    return document
