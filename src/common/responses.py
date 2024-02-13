import functools
import logging
import sys
import traceback
from collections.abc import Callable
from inspect import iscoroutinefunction
from typing import TypeVar
from uuid import uuid4

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
    400: {
        "model": ErrorResponse,
        "content": {"application/json": {"example": BadRequestException().dict()}},
    },
    401: {
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": ErrorResponse(
                    status=401,
                    type="UnauthorizedException",
                    message="Token validation failed",
                ).dict()
            }
        },
    },
    403: {
        "model": ErrorResponse,
        "content": {"application/json": {"example": MissingPrivilegeException().dict()}},
    },
    404: {
        "model": ErrorResponse,
        "content": {"application/json": {"example": NotFoundException().dict()}},
    },
    422: {
        "model": ErrorResponse,
        "content": {"application/json": {"example": ValidationException().dict()}},
    },
    500: {
        "model": ErrorResponse,
        "content": {"application/json": {"example": ApplicationException().dict()}},
    },
}

TResponse = TypeVar("TResponse", bound=Response)

"""
Function made to be used as a decorator for a route.
It will execute the function, and return a successful response of the passed response class.
If the execution fails, it will return a JSONResponse with a standardized error model.
"""


def create_response(
    response_class: type[TResponse] | None = None,
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
                error_response = ErrorResponse()
                if http_error.response:
                    error_response = ErrorResponse(
                        type="ExternalFetchException",
                        status=http_error.response.status_code,
                        message=http_error.response.text,
                        debug="Failed to fetch an external resource",
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
                logger.debug(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except NotFoundException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.debug(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_404_NOT_FOUND)
            except BadRequestException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.debug(e, extra={"Traceback": get_traceback()})
                logger.debug(e.dict())
                return JSONResponse(e.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except MissingPrivilegeException as e:
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.warning(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_403_FORBIDDEN)
            except ApplicationException as e:
                error_id = uuid4()
                if logger.level <= logging.DEBUG:
                    traceback.print_exc()
                logger.error(e, extra={"UUID": str(error_id), "Traceback": get_traceback()})
                return JSONResponse(e.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                error_id = uuid4()
                traceback.print_exc()
                logger.error(
                    f"Unexpected unhandled exception: {e}", extra={"UUID": str(error_id), "Traceback": get_traceback()}
                )
                return JSONResponse(
                    ErrorResponse().dict(),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return wrapper_decorator

    return func_wrapper


def get_traceback() -> str:
    """Get traceback as a log-friendly format."""
    exc_info = sys.exc_info()
    stack = traceback.extract_stack()
    tb = traceback.extract_tb(exc_info[2])
    full_tb = stack[:-1] + tb
    exc_line = traceback.format_exception_only(*exc_info[:2])
    return "Traceback (most recent call last):\n" + "".join(traceback.format_list(full_tb)) + "".join(exc_line)
