import unittest

from common.utils.data_structure.is_same import is_same


class IsSameTestCase(unittest.TestCase):
    def test_is_same(self):
        target = {"a": "1", "b": "2"}
        content = {"a": "1"}
        assert is_same(target, content)

    def test_is_not_same(self):
        target = {"a": "1", "b": "2"}
        content = {"a": "2"}
        assert is_same(target, content) is False
