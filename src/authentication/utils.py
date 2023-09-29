from typing import Dict, Set

from cachetools import TTLCache, cached

from authentication.models import PATData, User
from common.utils.logging import logger
from config import config
from enums import AuthProviderForRoleCheck
from services.azure_ad_get_app_role_assignments import get_azure_ad_app_role_assignments


@cached(cache=TTLCache(maxsize=32, ttl=600))
def _get_active_roles() -> Dict[str, Set[str]]:
    match config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        case AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY:
            return get_azure_ad_app_role_assignments()
    return {}


def extract_user_from_pat_data(pat_data: PATData) -> User:
    if not config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        logger.warn("PAT role assignment validation is not supported with the current OAuth provider.")
    elif config.TEST_TOKEN:
        logger.warn("PAT role assignment validation skipped due to 'TEST_TOKEN=True'")
    else:
        pat_roles: Set[str] = set(pat_data.roles)
        pat_data.roles = list(pat_roles.intersection(_get_active_roles()[pat_data.user_id]))
    user = User(**pat_data.dict())
    return user
