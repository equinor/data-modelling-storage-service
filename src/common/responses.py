import functools
import logging
import traceback
from inspect import iscoroutinefunction
from typing import Callable, Type, TypeVar

from pydantic import ValidationError
from requests import HTTPError
from starlette import status
from starlette.responses import JSONResponse, Response

from common.exceptions import (
    ApplicationException,
    BadRequestException,
    ErrorResponse,
    MissingPrivilegeException,
    NotFoundException,
    ValidationException,
)
from common.utils.logging import logger

responses = {
    400: {"model": ErrorResponse, "content": {"application/json": {"example": BadRequestException().dict()}}},
    401: {
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": ErrorResponse(
                    status=401, type="UnauthorizedException", message="Token validation failed"
                ).dict()
            }
        },
    },
    403: {"model": ErrorResponse, "content": {"application/json": {"example": MissingPrivilegeException().dict()}}},
    404: {"model": ErrorResponse, "content": {"application/json": {"example": NotFoundException().dict()}}},
    422: {"model": ErrorResponse, "content": {"application/json": {"example": ValidationException().dict()}}},
    500: {"model": ErrorResponse, "content": {"application/json": {"example": ApplicationException().dict()}}},
}

TResponse = TypeVar("TResponse", bound=Response)

"""
Function made to be used as a decorator for a route.
It will execute the function, and return a successful response of the passed response class.
If the execution fails, it will return a JSONResponse with a standardized error model.
"""


def create_response(  # noqa: C901
    response_class: Type[TResponse] | None = None,
) -> Callable[..., Callable[..., TResponse | JSONResponse]]:
    def func_wrapper(func) -> Callable[..., TResponse | JSONResponse]:
        @functools.wraps(func)
        async def wrapper_decorator(*args, **kwargs) -> TResponse | JSONResponse:
            try:
                # Await function if needed
                if not iscoroutinefunction(func):
                    result = func(*args, **kwargs)
                else:
                    result = await func(*args, **kwargs)
                if not response_class:  # If there is no response class, we create a 204 response (OK - no content)
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
                return response_class(result, status_code=200)
            except HTTPError as http_error:
                error_response = ErrorResponse(
                    type="ExternalFetchException",
                    status=http_error.response.status,
                    message="Failed to fetch an external resource",
                    debug=http_error.response,
                )
                logger.error(error_response)
                return JSONResponse(error_response.dict(), status_code=error_response.status)
            except ValidationError as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                validation_exception = ValidationException(message=str(e))
                return JSONResponse(validation_exception.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except ValidationException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.error(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except NotFoundException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.error(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_404_NOT_FOUND)
            except BadRequestException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.error(e)
                logger.error(e.dict())
                return JSONResponse(e.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except MissingPrivilegeException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.warning(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_403_FORBIDDEN)
            except ApplicationException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.error(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Unexpected unhandled exception: {e}")
                return JSONResponse(ErrorResponse().dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrapper_decorator

    return func_wrapper
