import unittest

from common.utils.data_structure.traverse import traverse_compare


class TraverseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_compare_lists_identical(self):
        actual = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value1"}]
        expected = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value1"}]
        result = traverse_compare(actual, expected)
        self.assertEqual(result, [])

    def test_compare_lists_different_entry(self):
        actual = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value1"}]
        expected = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value-1"}]
        result = traverse_compare(actual, expected)
        self.assertEqual(
            result,
            [
                {
                    "expected_value": "value-1",
                    "path": "[2].key1",
                    "actual_value": "value1",
                    "message": "Difference in primitive value",
                }
            ],
        )

    def test_compare_lists_missing_entry(self):
        actual = [{"key3": "value3"}, {"key2": "value2"}]
        expected = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value1"}]
        result = traverse_compare(actual, expected)
        self.assertEqual(
            result,
            [
                {
                    "expected_value": expected,
                    "path": "",
                    "actual_value": actual,
                    "message": "Actual length: 2. Expected length: 3",
                }
            ],
        )

    def test_compare_lists_extra_entry(self):
        actual = [{"key3": "value3"}, {"key2": "value2"}, {"key1": "value1"}]
        expected = [{"key3": "value3"}, {"key2": "value2"}]
        result = traverse_compare(actual, expected)
        self.assertEqual(
            result,
            [
                {
                    "expected_value": expected,
                    "path": "",
                    "actual_value": actual,
                    "message": "Actual length: 3. Expected length: 2",
                }
            ],
        )

    def test_compare_dicts_identical(self):
        actual = {"top": {"middle": {"nested": "value"}}}
        expected = {"top": {"middle": {"nested": "value"}}}
        self.assertEqual(traverse_compare(actual, expected), [])

    def test_compare_dicts_different_value(self):
        actual = {"top": {"middle": {"nested": "value"}}}
        expected = {"top": {"middle": {"nested": "wrong value"}}}
        self.assertEqual(
            traverse_compare(actual, expected),
            [
                {
                    "expected_value": "wrong value",
                    "path": "top.middle.nested",
                    "actual_value": "value",
                    "message": "Difference in primitive value",
                }
            ],
        )

    def test_compare_missing_key(self):
        actual = {"top": {"middle": {"nested": "value"}}}
        expected = {"top": {"middle": {"nested": "value", "nested2": "value2"}}}
        self.assertEqual(
            traverse_compare(actual, expected),
            [
                {
                    "expected_value": {"nested": "value", "nested2": "value2"},
                    "path": "top.middle",
                    "actual_value": {"nested": "value"},
                    "message": "Missing keys: nested2. Extra keys: ",
                }
            ],
        )

    def test_compare_extra_key(self):
        actual = {"top": {"middle": {"nested": "value", "nested2": "value2"}}}
        expected = {"top": {"middle": {"nested": "value"}}}
        self.assertEqual(
            traverse_compare(actual, expected),
            [
                {
                    "expected_value": {"nested": "value"},
                    "path": "top.middle",
                    "actual_value": {"nested": "value", "nested2": "value2"},
                    "message": "Missing keys: . Extra keys: nested2",
                }
            ],
        )
