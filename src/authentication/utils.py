from typing import Dict, Set

from authentication.models import PATData
from common.utils.logging import logger
from config import config


def remove_pat_roles_not_assigned_by_auth_provider(
    pat_data: PATData, application_role_assignments: Dict[str, Set[str]]
) -> PATData:
    """
    Takes app role assignments and removes roles in patData that are not defined by app role assignments.
    """
    if not config.AUTH_PROVIDER_FOR_ROLE_CHECK:
        logger.warn("PAT role assignment validation is not supported with the current OAuth provider.")
    elif config.TEST_TOKEN:
        logger.warn("PAT role assignment validation skipped due to 'TEST_TOKEN=True'")
    else:
        pat_roles: Set[str] = set(pat_data.roles)
        app_role_assignments_for_user = application_role_assignments[pat_data.user_id]
        pat_data.roles = list(pat_roles & app_role_assignments_for_user)
    return pat_data
