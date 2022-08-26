import functools
import traceback
from typing import Callable, Type, TypeVar
from inspect import iscoroutinefunction

from pydantic import ValidationError
from requests import HTTPError
from starlette import status
from starlette.responses import Response, JSONResponse

from common.exceptions import (
    MissingPrivilegeException,
    ValidationException,
    NotFoundException,
    BadRequestException,
    ErrorResponse,
)
from common.utils.logging import logger

TResponse = TypeVar("TResponse", bound=Response)

"""
Function made to be used as a decorator for a route.
It will execute the function, and return a successful response of the passed response class.
If the execution fails, it will return a JSONResponse with a standardized error model.
"""


def create_response(response_class: Type[TResponse]) -> Callable[..., Callable[..., TResponse | JSONResponse]]:
    def func_wrapper(func) -> Callable[..., TResponse | JSONResponse]:
        @functools.wraps(func)
        async def wrapper_decorator(*args, **kwargs) -> TResponse | JSONResponse:
            try:
                # Await function if needed
                if not iscoroutinefunction(func):
                    result = func(*args, **kwargs)
                else:
                    result = await func(*args, **kwargs)
                return response_class(result, status_code=200)
            except HTTPError as http_error:
                error_response = ErrorResponse(
                    status=http_error.response.status,
                    userMessage="Failed to fetch an external resource",
                    developerMessage=http_error.response
                )
                logger.error(error_response)
                return JSONResponse(error_response.dict(), status_code=error_response.status)
            except (ValidationError, ValidationException) as e:
                logger.error(e)
                return JSONResponse(e.dict(),  status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except NotFoundException as e:
                logger.error(e)
                return JSONResponse(e.dict(), status_code=status.HTTP_404_NOT_FOUND)
            except BadRequestException as e:
                logger.error(e)
                logger.error(e.dict())
                return JSONResponse(e.dict(), status_code=status.HTTP_400_BAD_REQUEST)
            except MissingPrivilegeException as e:
                logger.warning(e)
                return JSONResponse(e.dict(),  status_code=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Unexpected unhandled exception: {e}")
                return JSONResponse(ErrorResponse().dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrapper_decorator

    return func_wrapper
