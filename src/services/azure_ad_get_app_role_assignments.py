from typing import Dict, List, Set

from cachetools import TTLCache, cached

from common.utils.graph_api_client import (
    AppRoleAssignment,
    get_app_roles,
    get_app_roles_assigned_to,
)
from config import config
from enums import AuthProviderForRoleCheck


@cached(cache=TTLCache(maxsize=32, ttl=600))
def get_active_roles() -> Dict[str, Set[str]]:
    match config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        case AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY:
            return get_azure_ad_app_role_assignments()
    return {}


def get_azure_ad_app_role_assignments() -> Dict[str, Set[str]]:
    """
    Get a dictionary of assigned app roles for the Azure AD enterprise app,
    where the key is a user's user_id and the value is a list of currently assigned roles
    """
    DEFAULT_ACCESS_ROLE_ID: str = "00000000-0000-0000-0000-000000000000"
    assignments: Dict[str, Set[str]] = {}
    app_roles: Dict[str, str] = {role.id: role.value for role in get_app_roles()}

    all_assigned_roles: List[AppRoleAssignment] = get_app_roles_assigned_to()
    for app_role_assignment in all_assigned_roles:
        user_id: str = app_role_assignment.principalId
        app_role_id: str = app_role_assignment.appRoleId
        # Ignore 'Default Access' role
        if app_role_id == DEFAULT_ACCESS_ROLE_ID:
            continue

        if user_id not in assignments:
            assignments[user_id] = set()
        assignments[user_id].add(app_roles[app_role_id])

    return assignments
