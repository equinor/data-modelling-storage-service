import unittest

from common.utils.encryption import scrypt


class HasingTestCase(unittest.TestCase):
    salt = "arandomgeneratedstring"
    value1 = "My string to hash."
    value2 = "Another string."

    def test_hashing_returns_same_with_same_value_and_same_salt(self):
        digest1 = scrypt(self.value1, self.salt)
        digest2 = scrypt(self.value1, self.salt)
        assert digest1 == digest2

    def test_hashing_returns_different_with_different_salt_and_same_value(self):
        digest1 = scrypt(self.value1, self.salt)
        digest2 = scrypt(self.value1, "another salt")
        assert digest1 != digest2

    def test_hashing_returns_different_with_different_value_and_same_salt(self):
        digest1 = scrypt(self.value1, self.salt)
        digest2 = scrypt(self.value2, self.salt)
        assert digest1 != digest2

    def test_hashing_output_has_equal_length_for_different_input(self):
        digest1 = scrypt(self.value1, self.salt)
        digest2 = scrypt(self.value2, self.salt)
        assert len(digest1) == len(digest2)

    def test_hashing_output_not_contain_the_values_or_salt(self):
        digest = scrypt(self.value1, self.salt)
        assert self.value1 not in digest
        assert self.salt not in digest
