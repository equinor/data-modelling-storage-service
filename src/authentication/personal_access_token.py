import datetime
from typing import Dict, Set

from cachetools import TTLCache, cached
from fastapi import HTTPException
from starlette import status

from authentication import get_app_role_assignments
from authentication.models import AccessLevel, PATData, User
from common.utils.encryption import generate_key, scrypt
from common.utils.logging import logger
from config import config
from enums import AuthProviderForRoleCheck
from storage.internal.personal_access_tokens import insert_pat

MAX_TOKEN_TTL = datetime.timedelta(days=365).total_seconds()


@cached(cache=TTLCache(maxsize=32, ttl=600))
def get_active_roles() -> Dict[str, Set[str]]:
    match config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        case AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY:
            return get_app_role_assignments.get_app_role_assignments_azure_ad()
    return {}


def create_personal_access_token(
    user: User, scope: AccessLevel = AccessLevel.WRITE, ttl: int = int(datetime.timedelta(days=30).total_seconds())
) -> str:
    """
    Create a time limited personal access token that can be used to impersonate the user requesting the token.
    Scope can be defined to limit the PAT's permission to read-only, and TTL (time-to-live in seconds) can be reduced,
    or extended up to 1 year. Default 1 month.
    The PAT's hash is stored in the internal DB's PAT collection.
    """
    if not isinstance(scope, AccessLevel):
        raise ValueError("Scope on a personal access token must be one of (NONE, READ, WRITE)")
    if ttl <= 0 or ttl > MAX_TOKEN_TTL:
        raise ValueError(
            f"Validity time of a personal access token must be between '1' and '{MAX_TOKEN_TTL}' seconds."
        )
    now = datetime.datetime.now()
    expire_datetime = now + datetime.timedelta(seconds=ttl)
    pat = f"DMSS_{generate_key()}"  # Generate a random string, this will be the actual token.
    pat_data = PATData(  # Create a PAT object with parameters, and the hash of the token.
        pat_hash=scrypt(pat), user_id=user.user_id, roles=user.roles, scope=scope, expire=expire_datetime
    )
    insert_pat(pat_data)  # Save the PAT Object to the database
    return pat  # Return the secret


def extract_user_from_pat_data(pat_data: PATData) -> User:
    if datetime.datetime.now() > pat_data.expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Personal Access Token expired",
            headers={"WWW-Authenticate": "Access-Key"},
        )
    if not config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        logger.warn("PAT role assignment validation is not supported with the current OAuth provider.")
    elif config.TEST_TOKEN:
        logger.warn("PAT role assignment validation skipped due to 'TEST_TOKEN=True'")
    else:
        pat_roles: Set[str] = set(pat_data.roles)
        pat_data.roles = list(pat_roles.intersection(get_active_roles()[pat_data.user_id]))
    user = User(**pat_data.dict())
    return user
