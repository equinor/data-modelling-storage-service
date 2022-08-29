import unittest
from authentication.models import AccessLevel


class DataSourceTestCase(unittest.TestCase):
    def test_save_into_multiple_repositories(self):
        write = AccessLevel.WRITE
        read = AccessLevel.READ
        none = AccessLevel.NONE

        if not ((write > read and write > none) and (read < write and read > none) and (none < write and none < read)):
            raise Exception("Error with comparing access levels!")
