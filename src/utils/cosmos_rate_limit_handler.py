import re
import time
from pymongo.errors import OperationFailure

from utils.logging import logger


def get_retry_after(error: OperationFailure) -> int:
    error_code = error.code
    if error_code == 16500:
        if error_message := error.details.get("errmsg"):
            retry_after = 500  # retry after 500ms by default
            try:
                pattern = r"RetryAfterMs=[0-9]{1,},"
                match = re.search(pattern, error_message)
                if match:
                    _retry_after = int(match.group().split("=")[1].strip(","))
                    if isinstance(_retry_after, int):
                        retry_after = _retry_after
            except Exception:
                logger.warn(
                    "Failed to parse 'RetryAfterMs' from the CosmosDB error details. Falling back to default timeout."
                )
        logger.warn(
            "Received 429 TooManyRequests (Rate-Limited) response from CosmosDB. "
            f"Sleeping for {retry_after}ms before retrying."
        )
        return retry_after / 1000
    return 0


def rate_limit_handler(func):
    """
    Decorator to help handle CosmosDB 429 errors (rate limit exceeded)
    """

    def wrapper(*arg):
        try:
            return func(*arg)
        except OperationFailure as error:
            retry_after = get_retry_after(error)
            if retry_after > 0:
                time.sleep(retry_after)
                return func(*arg)
            else:
                raise error

    return wrapper
