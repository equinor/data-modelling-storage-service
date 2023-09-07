import unittest

from common.utils.encryption import scrypt


class HasingTestCase(unittest.TestCase):
    salt = "arandomgeneratedstring"

    def test_hasing_returns_same_with_same_value_and_same_salt(self):
        value = "My string to hash"
        digest = scrypt(value, self.salt)
        digest2 = scrypt(value, self.salt)
        assert digest == digest2

    def test_hashing_returns_different_with_different_salt_and_same_value(self):
        value = "My string to hash"
        digest = scrypt(value, self.salt)
        digest2 = scrypt(value, "another salt")
        assert digest != digest2

    def test_hashing_returns_different_with_different_value_and_same_salt(self):
        value1 = "My string to hash."
        value2 = "Another string."
        digest = scrypt(value1, self.salt)
        digest2 = scrypt(value2, self.salt)
        assert digest != digest2
