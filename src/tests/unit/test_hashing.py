import unittest

from utils.encryption import scrypt


class HasingTestCase(unittest.TestCase):
    salt = "arandomgeneratedstring"

    def test_scrypt(self):
        value = "My string to hash"
        digest = scrypt(value, self.salt)
        digest2 = scrypt(value, self.salt)
        assert digest == digest2
