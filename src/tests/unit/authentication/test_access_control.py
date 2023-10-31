import unittest

from authentication.access_control import assert_user_has_access
from authentication.models import AccessControlList, AccessLevel, User
from common.exceptions import MissingPrivilegeException
from config import config


class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.OWNER_ID = "1"
        self.user = User(user_id="0", roles=[], scope=AccessLevel.WRITE)
        self.mock_acl = AccessControlList(
            owner=self.OWNER_ID,
            roles={
                "reader": AccessLevel.READ,
                "writer": AccessLevel.WRITE,
                "no-access": AccessLevel.NONE,
            },
            others=AccessLevel.READ,
        )
        self.original_config = config.copy()
        config.AUTH_ENABLED = True
        config.DMSS_ADMIN = self.OWNER_ID
        config.DMSS_ADMIN_ROLE = "admin_role"

    def tearDown(self) -> None:
        """This is required to reset the external config object back to default."""
        config.AUTH_ENABLED = self.original_config.AUTH_ENABLED
        config.DMSS_ADMIN = self.original_config.DMSS_ADMIN
        config.DMSS_ADMIN_ROLE = self.original_config.DMSS_ADMIN_ROLE

    def test_assert_user_has_access_when_auth_is_disabled(self):
        config.AUTH_ENABLED = False
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=None)
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.READ, user=None)
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.NONE, user=None)

    def test_assert_MissingPrivilegeException_when_user_scope_is_insufficient(self):
        self.user.scope = AccessLevel.NONE
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.READ, user=self.user)
        self.user.scope = AccessLevel.READ
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=self.user)

    def test_assert_user_has_read_access_when_nothing_is_specified_and_other_is_read(self):
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.READ, user=self.user)
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=self.user)

    def test_assert_MissingPrivilegeException_when_nothing_is_specified_and_default_other_is_NONE(self):
        self.mock_acl.others = AccessLevel.NONE
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.READ, user=self.user)

    def test_user_has_write_access_when_nothing_is_specified_and_default_other_is_WRITE(self):
        self.mock_acl.others = AccessLevel.WRITE
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=self.user)

    def test_assert_user_has_write_access_when_user_is_owner(self):
        user = User(user_id=self.OWNER_ID)
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=user)

    def test_assert_user_has_access_when_specified_with_role(self):
        self.user.roles = ["reader"]
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.READ, user=self.user)

    def test_assert_MissingPrivilegeException_when_specified_with_insufficient_role(self):
        self.user.roles = ["reader"]
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=self.user)

    def test_user_has_access_when_user_id_has_access_in_acl(self):
        self.mock_acl.users.update({"id123": AccessLevel.WRITE})
        user = User(user_id="id123")
        assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=user)

    def test_assert_MissingPrivilegeException_when_user_id_has_access_in_acl_but_with_insufficient_privilege(self):
        self.mock_acl.users.update({"id123": AccessLevel.READ})
        user = User(user_id="id123")
        with self.assertRaises(MissingPrivilegeException):
            assert_user_has_access(acl=self.mock_acl, access_level_required=AccessLevel.WRITE, user=user)


if __name__ == "__main__":
    unittest.main()
