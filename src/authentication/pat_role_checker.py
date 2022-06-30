from cachetools import cached, TTLCache
from typing import Dict, Set

from utils.graph_api_client import get_app_roles, get_app_roles_assigned_to
from utils.logging import logger

DEFAULT_ACCESS_ROLE_ID: str = "00000000-0000-0000-0000-000000000000"


@cached(cache=TTLCache(maxsize=32, ttl=3600))
def get_app_role_assignments_azure_ad() -> Dict[str, Set[str]]:
    """
    Get a dictionary of assigned app roles for the Azure AD enterprise app,
    where they key is a user's user_id and the value is a list of still assigned roles
    """
    assignments = {}
    all_app_roles = get_app_roles()
    all_assigned_roles = get_app_roles_assigned_to()
    for app_role_assignment in all_assigned_roles:
        user_id = app_role_assignment.principalId
        app_role_id = app_role_assignment.appRoleId
        # Ignore 'Default Access' role
        if app_role_id != DEFAULT_ACCESS_ROLE_ID:
            if user_id not in assignments:
                assignments[user_id] = set()
            # Get the app role definition
            app_role_definition = next(
                filter(lambda app_role_definition: app_role_definition.id == app_role_id, all_app_roles), None
            )
            if app_role_definition:
                app_role_name = app_role_definition.value
                assignments[user_id].add(app_role_name)
            else:
                logger.warn(f"Failed to determine name of App Role with ID '{app_role_id}'.")

    return assignments
