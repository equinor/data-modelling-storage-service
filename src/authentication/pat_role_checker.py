from cachetools import cached, TTLCache
from typing import Dict, Set

from utils.graph_api_client import get_app_roles, get_app_roles_assigned_to


@cached(cache=TTLCache(maxsize=32, ttl=3600))
def get_app_role_lookup() -> Dict[str, str]:
    """
    Get a dictionary of all defined app roles for the Azure AD enterprise app,
    where the key is an app role's ID and the value is the app role's value (name)
    """
    app_role_map = {}
    all_app_roles = get_app_roles()
    for app_role_definition in all_app_roles:
        app_role_map[app_role_definition.id] = app_role_definition.value

    return app_role_map


@cached(cache=TTLCache(maxsize=32, ttl=3600))
def get_app_role_assignments_azure_ad() -> Dict[str, Set[str]]:
    """
    Get a dictionary of assigned app roles for the Azure AD enterprise app,
    where the key is a user's user_id and the value is a list of currently assigned roles
    """
    DEFAULT_ACCESS_ROLE_ID: str = "00000000-0000-0000-0000-000000000000"
    assignments = {}
    app_roles = get_app_role_lookup()
    all_assigned_roles = get_app_roles_assigned_to()
    for app_role_assignment in all_assigned_roles:
        user_id = app_role_assignment.principalId
        app_role_id = app_role_assignment.appRoleId
        # Ignore 'Default Access' role
        if app_role_id == DEFAULT_ACCESS_ROLE_ID:
            continue

        if user_id not in assignments:
            assignments[user_id] = set()
        assignments[user_id].add(app_roles[app_role_id])

    return assignments
