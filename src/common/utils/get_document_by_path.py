from typing import Union

from authentication.models import User
from common.exceptions import BadRequestException, NotFoundException
from common.utils.resolve_reference import resolve_reference
from common.utils.string_helpers import split_dmss_ref
from storage.internal.data_source_repository import get_data_source


def get_document_uid_by_path(dotted_path: str, data_source_id: str, user: User) -> Union[str, None]:
    data_source = get_data_source(data_source_id, user)
    document = resolve_reference(
        dotted_path, data_source, lambda data_source_name: get_data_source(data_source_name, user)
    )
    return document["_id"]


def get_document_by_absolute_path(absolute_path: str, user: User) -> dict:
    """Fetches the document from any supported protocol by the absolute path which must be on the format
    PROTOCOL://ADDRESS"""

    try:
        protocol, address = absolute_path.split("://", 1)
    except ValueError:
        raise BadRequestException(f"Invalid format. The value '{absolute_path}' does not specify a protocol.")
    match protocol:
        case "dmss":  # The entity should be fetched from a DataSource in this DMSS instance
            data_source_id, path, attribute = split_dmss_ref(address)
            if not path:
                raise BadRequestException(f"The path '{absolute_path}' is an invalid document reference.")
            document_repository = get_data_source(data_source_id, user)
            try:
                document = resolve_reference(
                    f"/{path}", document_repository, lambda data_source_name: get_data_source(data_source_name, user)
                )
                type_id = document["_id"]
            except NotFoundException as error:
                raise NotFoundException(
                    message=f"Entity referenced with '{absolute_path}' could not be found",
                    debug=error.message,
                    data=error.dict(),
                )
            return document_repository.get(uid=type_id)
        case "http":  # The entity should be fetched by an HTTP call
            raise NotImplementedError
        case _:
            raise NotImplementedError
