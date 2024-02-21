import unittest

from authentication.models import AccessControlList, AccessLevel, User
from config import config


class AccessControlListTestCase(unittest.TestCase):
    def setUp(self):
        self.acl = AccessControlList(owner="user1", roles={"role1": AccessLevel.WRITE}, others=AccessLevel.READ)

    def test_initialization(self):
        self.assertEqual(self.acl.owner, "user1")
        self.assertEqual(self.acl.roles, {"role1": AccessLevel.WRITE})
        self.assertEqual(self.acl.users, {})
        self.assertEqual(self.acl.others, AccessLevel.READ)

    def test_add_role(self):
        self.acl.roles["role2"] = AccessLevel.READ
        self.assertEqual(self.acl.roles, {"role1": AccessLevel.WRITE, "role2": AccessLevel.READ})

    def test_add_user(self):
        self.acl.users["user2"] = AccessLevel.WRITE
        self.assertEqual(self.acl.users, {"user2": AccessLevel.WRITE})

    def test_generate_dict(self):
        expected_dict = {
            "owner": "user1",
            "roles": {"role1": "WRITE"},
            "users": {},
            "others": "READ",
        }
        acl_dict = self.acl.to_dict()
        self.assertEqual(acl_dict, expected_dict)

    def test_default(self):
        acl = AccessControlList.default()

        self.assertEqual(acl.owner, config.DMSS_ADMIN)
        self.assertEqual(acl.roles, {config.DMSS_ADMIN_ROLE: AccessLevel.WRITE})
        self.assertEqual(acl.others, AccessLevel.READ)

    def test_default_with_owner_returns_acl_with_user_as_owner(self):
        user = User(user_id="123")
        acl = AccessControlList.default_with_owner(user)
        self.assertEqual(acl.owner, user.user_id)


if __name__ == "__main__":
    unittest.main()
