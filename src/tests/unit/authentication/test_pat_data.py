import unittest
from datetime import UTC, datetime
from uuid import UUID

from authentication.models import AccessLevel, PATData


class PatDataTestCase(unittest.TestCase):
    def test_init(self):
        expire = datetime.now(UTC)

        pat_data = PATData(
            pat_hash="hash123",
            user_id="user1",
            roles=["role1", "role2"],
            scope=AccessLevel.READ,
            expire=expire,
        )
        self.assertEqual(pat_data.pat_hash, "hash123")
        self.assertEqual(pat_data.user_id, "user1")
        self.assertEqual(pat_data.roles, ["role1", "role2"])
        self.assertEqual(pat_data.scope, AccessLevel.READ)
        self.assertEqual(pat_data.expire, expire)
        self.assertIsNotNone(pat_data.uuid)

    def test_dict(self):
        pat_data = PATData(
            pat_hash="hash123",
            user_id="user1",
            roles=["role1", "role2"],
            scope=AccessLevel.READ,
            expire=datetime.now(UTC),
        )
        as_dict = pat_data.dict()
        self.assertEqual(as_dict["_id"], "hash123")
        self.assertEqual(as_dict["user_id"], "user1")
        self.assertEqual(as_dict["roles"], ["role1", "role2"])
        self.assertEqual(as_dict["scope"], AccessLevel.READ)

    def test_uuid_default(self):
        pat_data = PATData(user_id="user1", scope=AccessLevel.WRITE, expire=datetime.now(UTC))

        self.assertIsInstance(pat_data.uuid, str)
        try:
            UUID(pat_data.uuid, version=4)  # see if we can cast it to uuid.
        except ValueError:
            self.fail(f"Was not able to cast {pat_data.uuid} to UUID, and therefore it is not a valid UUID string. ")
