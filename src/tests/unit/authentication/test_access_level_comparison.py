import unittest

from authentication.models import AccessLevel

WRITE = AccessLevel.WRITE
READ = AccessLevel.READ
NONE = AccessLevel.NONE


class TestAccessLevel(unittest.TestCase):
    def test_access_level_comparison_true(self):
        self.assertTrue(WRITE == WRITE)
        self.assertTrue(READ == READ)
        self.assertTrue(NONE == NONE)

        self.assertTrue(NONE < READ)
        self.assertTrue(READ < WRITE)

    def test_access_level_comparison_false(self):
        self.assertFalse(WRITE < READ)
        self.assertFalse(WRITE < NONE)
        self.assertFalse(READ < NONE)

    def test_check_privilege_should_be_true(self):
        self.assertTrue(WRITE.check_privilege(required_level=WRITE))
        self.assertTrue(WRITE.check_privilege(required_level=READ))
        self.assertTrue(WRITE.check_privilege(required_level=NONE))

        self.assertTrue(READ.check_privilege(required_level=READ))
        self.assertTrue(READ.check_privilege(required_level=NONE))

        self.assertTrue(NONE.check_privilege(required_level=NONE))

    def test_check_privilege_false(self):
        self.assertFalse(READ.check_privilege(required_level=WRITE))

        self.assertFalse(NONE.check_privilege(required_level=READ))
        self.assertFalse(NONE.check_privilege(required_level=WRITE))

    def test_check_privilege_invalid_input(self):
        with self.assertRaises(AttributeError):
            WRITE.check_privilege("INVALID")
        with self.assertRaises(AttributeError):
            WRITE.check_privilege(0)


if __name__ == "__main__":
    unittest.main()
