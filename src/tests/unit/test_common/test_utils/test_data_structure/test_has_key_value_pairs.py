import unittest

from common.utils.data_structure.has_key_value_pairs import has_key_value_pairs


class HasKeyValuePairsTestCase(unittest.TestCase):
    def setUp(self):
        self.target = {"a": "1", "b": "2"}

    def test_target_contains_key_value_pair_returns_true(self):
        assert has_key_value_pairs(self.target, {"a": "1"})
        assert has_key_value_pairs(self.target, {"b": "2"})

    def test_target_not_contains_key_value_pair_returns_false(self):
        assert has_key_value_pairs(self.target, {"a": "2"}) is False
        assert has_key_value_pairs(self.target, {"b": "1"}) is False
