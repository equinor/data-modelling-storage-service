import unittest

from authentication.models import AccessControlList, AccessLevel


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
        acl_dict = self.acl.dict()
        self.assertEqual(acl_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
