import unittest

from authentication.models import AccessLevel, User


class TestUser(unittest.TestCase):
    def test_create_user(self):
        user = User(user_id="123")
        self.assertEqual(user.user_id, "123")
        self.assertIsNone(user.email)
        self.assertIsNone(user.full_name)
        self.assertEqual(user.roles, [])
        self.assertEqual(user.scope, AccessLevel.WRITE)

    def test_hash(self):
        user1 = User(user_id="123")
        user2 = User(user_id="123")
        user3 = User(user_id="456")

        self.assertEqual(hash(user1), hash(user2))
        self.assertNotEqual(hash(user1), hash(user3))

    def test_email(self):
        user = User(user_id="123", email="user@example.com")
        self.assertEqual(user.email, "user@example.com")

    def test_full_name(self):
        user = User(user_id="123", full_name="Harry Potter")
        self.assertEqual(user.full_name, "Harry Potter")

    def test_roles(self):
        user = User(user_id="123", roles=["admin", "user"])
        self.assertEqual(user.roles, ["admin", "user"])

    def test_scope(self):
        user = User(user_id="123", scope=AccessLevel.READ)
        self.assertEqual(user.scope, AccessLevel.READ)

    def test_default(self):
        user = User.default()

        self.assertEqual(user.user_id, "nologin")
        self.assertEqual(user.full_name, "Not Authenticated")
        self.assertEqual(user.email, "nologin@example.com")


if __name__ == "__main__":
    unittest.main()
