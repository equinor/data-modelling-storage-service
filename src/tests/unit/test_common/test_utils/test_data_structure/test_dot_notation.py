import unittest

from common.utils.data_structure.dot_notation import (
    get_by_dot,
    to_dot_notation,
    to_path,
)


class DotNotationTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_to_dot_notation_when_dict_returns_dotted_string(self):
        path = ["top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "top.middle.nested")

    def test_to_dot_notation_when_list_returns_dotted_string(self):
        path = ["[0]", "top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "[0].top.middle.nested")

    def test_to_dot_notation_when_nested_list_returns_dotted_string(self):
        path = ["top", "list", "[0]", "top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "top.list[0].top.middle.nested")

    def test_to_path_when_dict_returns_array_of_strings(self):
        dot_path = "top.middle.nested"
        self.assertEqual(to_path(dot_path), ["top", "middle", "nested"])

    def test_to_path_when_list_returns_array_of_strings(self):
        dot_path = "[0].top.middle.nested"
        self.assertEqual(to_path(dot_path), ["[0]", "top", "middle", "nested"])

    def test_to_path_when_nested_list_returns_array_of_strings(self):
        dot_path = "top.list[0].top.middle.nested"
        self.assertEqual(to_path(dot_path), ["top", "list", "[0]", "top", "middle", "nested"])

    def test_get_by_dot_notation_when_dict_returns_correct_value(self):
        nested_dict = {
            "top": {
                "middle": {"nested": "value"},
                "list": [{"top": {"middle": {"nested": "value 1"}}}, {"top": {"middle": {"nested": "value 2"}}}],
            }
        }
        self.assertEqual(get_by_dot(nested_dict, "top.middle.nested"), "value")
        self.assertEqual(get_by_dot(nested_dict, "top.list[0].top.middle.nested"), "value 1")
        self.assertEqual(get_by_dot(nested_dict, "top.list[1].top.middle.nested"), "value 2")
        self.assertRaises(IndexError, get_by_dot, nested_dict, "top.list[2]")
        self.assertRaises(KeyError, get_by_dot, nested_dict, "top.middle.unknown")

    def test_get_by_dot_notation_when_list_returns_correct_value(self):
        list_of_nested_dicts = [
            {
                "top": {
                    "middle": {"nested": "value"},
                    "list": [{"top": {"middle": {"nested": "value 1"}}}, {"top": {"middle": {"nested": "value 2"}}}],
                }
            },
            {
                "top": {
                    "middle": {"nested": "value"},
                    "list": [{"top": {"middle": {"nested": "value 1"}}}, {"top": {"middle": {"nested": "value 2"}}}],
                }
            },
        ]
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[0].top.middle.nested"), "value")
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[0].top.list[0].top.middle.nested"), "value 1")
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[0].top.list[1].top.middle.nested"), "value 2")
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[1].top.middle.nested"), "value")
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[1].top.list[0].top.middle.nested"), "value 1")
        self.assertEqual(get_by_dot(list_of_nested_dicts, "[1].top.list[1].top.middle.nested"), "value 2")
        self.assertRaises(IndexError, get_by_dot, list_of_nested_dicts, "[2]")
        self.assertRaises(KeyError, get_by_dot, list_of_nested_dicts, "[0].top.middle.unknown")
