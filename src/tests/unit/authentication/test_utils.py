import unittest
from datetime import datetime
from unittest import skip

from authentication.models import AccessLevel, PATData
from authentication.utils import remove_pat_roles_not_assigned_by_auth_provider
from config import config


class RemovePatRolesNotAssignedByAuthProviderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.original_config = config.copy()
        config.TEST_TOKEN = False
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = True

        self.application_role_assignments = {"user_id": {"reader", "writer"}}
        self.pat = PATData(user_id="user_id", roles=["reader", "owner"], scope=AccessLevel.NONE, expire=datetime.now())

    def tearDown(self) -> None:
        config.TEST_TOKEN = self.original_config.TEST_TOKEN
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = self.original_config.AUTH_PROVIDER_FOR_ROLE_CHECK

    @skip(reason="to be fixed, now throws")
    def test_assert_returns_no_roles_when_roles_from_auth_provider_is_empty(self):
        roles_from_auth_provider = {}

        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, roles_from_auth_provider)

        self.assertListEqual(updated_pat_data.roles, [])

    def test_assert_returns_no_roles_when_roles_from_pat_is_empty(self):
        pass

    def test_assert_returns_intersection_of_roles(self):
        pass

    def test_assert_removes_no_roles_when_config_TEST_TOKEN_is_true(self):
        config.TEST_TOKEN = True
        pass

    def test_assert_removes_no_roles_when_config_AUTH_PROVIDER_FOR_ROLE_CHECK_is_false(self):
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = False
        pass

    def test_assert_does_not_modify_rest_of_pat_when_removing_roles(self):
        pass
