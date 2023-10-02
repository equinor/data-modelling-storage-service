from typing import Set

from authentication.models import PATData
from common.utils.logging import logger
from config import config
from services.role_assignments_provider import RoleAssignmentsProvider


def remove_pat_roles_not_assigned_by_auth_provider(
    pat_data: PATData, role_assignments_provider: RoleAssignmentsProvider
) -> PATData:
    """
    Takes app role assignments and removes roles in pat_data that are not defined by app role assignments.
    """
    if not config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        logger.warning("PAT role assignment validation is not supported with the current OAuth provider.")
    elif config.TEST_TOKEN:
        logger.warning("PAT role assignment validation skipped due to 'TEST_TOKEN=True'")
    else:
        pat_roles: Set[str] = set(pat_data.roles)
        application_role_assignments: dict[str, set[str]] = role_assignments_provider.get_assignments()
        app_role_assignments_for_user = application_role_assignments.get(pat_data.user_id, set())
        pat_data.roles = list(pat_roles & app_role_assignments_for_user)
    return pat_data
