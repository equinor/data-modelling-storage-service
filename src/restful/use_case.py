import traceback

from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse, PlainTextResponse

from utils.exceptions import (
    BadRequestException,
    DataSourceAlreadyExistsException,
    DataSourceNotFoundException,
    DuplicateFileNameException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    FileNotFoundException,
    InvalidChildTypeException,
    InvalidDocumentNameException,
    InvalidEntityException,
    InvalidSortByAttributeException,
    MissingPrivilegeException,
    RootPackageNotFoundException,
    ValidationException,
)
from utils.logging import logger


def create_error_response(
    error: Exception,
    status: int,
) -> JSONResponse:
    types = {
        404: "RESOURCE_ERROR",
        400: "PARAMETERS_ERROR",
        422: "UNPROCESSABLE_ENTITY",
        500: "SYSTEM_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
    }

    return JSONResponse({"type": types[status], "message": f"{error.__class__.__name__}: {error.message}"}, status)


class UseCase:
    def execute(self, request_object=None):
        try:
            return self.process_request(request_object)
        except (
            EntityNotFoundException,
            DataSourceNotFoundException,
            RootPackageNotFoundException,
            FileNotFoundException,
        ) as e:
            logger.warning(e)
            return create_error_response(e, status.HTTP_404_NOT_FOUND)
        except (
            EntityAlreadyExistsException,
            InvalidDocumentNameException,
            InvalidEntityException,
            ValidationError,
            ValidationException,
        ) as e:
            logger.error(e)
            return create_error_response(e, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except MissingPrivilegeException as e:
            return create_error_response(e, status.HTTP_403_FORBIDDEN)
        except (
            DataSourceAlreadyExistsException,
            InvalidSortByAttributeException,
            BadRequestException,
            DuplicateFileNameException,
            InvalidChildTypeException,
        ) as e:
            return create_error_response(e, status.HTTP_400_BAD_REQUEST)
        except Exception:
            traceback.print_exc()
            return PlainTextResponse("Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")
