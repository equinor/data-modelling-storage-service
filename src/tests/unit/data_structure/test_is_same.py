import unittest

from common.utils.data_structure.has_key_value_pairs import has_key_value_pairs


class IsSameTestCase(unittest.TestCase):
    def test_is_same(self):
        target = {"a": "1", "b": "2"}
        content = {"a": "1"}
        assert has_key_value_pairs(target, content)

    def test_is_not_same(self):
        target = {"a": "1", "b": "2"}
        content = {"a": "2"}
        assert has_key_value_pairs(target, content) is False
