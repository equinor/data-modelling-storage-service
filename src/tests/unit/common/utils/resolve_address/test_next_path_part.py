import unittest

from common.providers.address_resolver import _next_path_part


class NextPartPathTestCase(unittest.TestCase):
    def test_next_reference_item(self):
        # Example 0
        self.assertEqual(_next_path_part("$1"), ("$1", None, ""))

        # Example 1
        self.assertEqual(_next_path_part("/$1"), ("", "/", "$1"))
        self.assertEqual(_next_path_part("$1"), ("$1", None, ""))

        # Example 2
        self.assertEqual(_next_path_part("/root/package/$1"), ("", "/", "root/package/$1"))
        self.assertEqual(_next_path_part("root/package/$1"), ("root", "/", "package/$1"))
        self.assertEqual(_next_path_part("package/$1"), ("package", "/", "$1"))
        self.assertEqual(_next_path_part("$1"), ("$1", None, ""))
