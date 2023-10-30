import unittest
from datetime import datetime
from unittest import mock

from authentication.models import AccessLevel, PATData
from authentication.utils import remove_pat_roles_not_assigned_by_auth_provider
from config import config
from enums import AuthProviderForRoleCheck


class RemovePatRolesNotAssignedByAuthProviderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.original_config = config.model_copy()
        config.TEST_TOKEN = False
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY

        self.mock_role_provider = mock.Mock()
        self.mock_role_provider.get_assignments.return_value = {"user_id": {"reader", "writer"}}
        self.pat = PATData(user_id="user_id", roles=["reader", "owner"], scope=AccessLevel.NONE, expire=datetime.now())

    def tearDown(self) -> None:
        config.TEST_TOKEN = self.original_config.TEST_TOKEN
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = self.original_config.AUTH_PROVIDER_FOR_ROLE_CHECK

    def test_assert_returns_no_roles_when_roles_from_auth_provider_is_empty(self):
        self.mock_role_provider.get_assignments.return_value = {}

        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)

        self.assertListEqual(updated_pat_data.roles, [])

    def test_assert_returns_no_roles_when_roles_from_pat_is_empty(self):
        self.pat.roles = []

        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)

        self.assertListEqual(updated_pat_data.roles, [])

    def test_assert_returns_intersection_of_roles(self):
        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)
        self.assertListEqual(updated_pat_data.roles, ["reader"])

    def test_assert_removes_no_roles_when_config_TEST_TOKEN_is_true(self):
        config.TEST_TOKEN = True
        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)

        self.assertListEqual(updated_pat_data.roles, self.pat.roles)

    def test_assert_removes_no_roles_when_config_AUTH_PROVIDER_FOR_ROLE_CHECK_is_false(self):
        config.AUTH_PROVIDER_FOR_ROLE_CHECK = False
        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)

        self.assertListEqual(updated_pat_data.roles, self.pat.roles)

    def test_assert_does_not_modify_rest_of_pat_when_removing_roles(self):
        updated_pat_data = remove_pat_roles_not_assigned_by_auth_provider(self.pat, self.mock_role_provider)

        self.assertEqual(updated_pat_data.pat_hash, self.pat.pat_hash)
        self.assertEqual(updated_pat_data.user_id, self.pat.user_id)
        self.assertEqual(updated_pat_data.scope, self.pat.scope)
        self.assertEqual(updated_pat_data.expire, self.pat.expire)
        self.assertEqual(updated_pat_data.uuid, self.pat.uuid)
