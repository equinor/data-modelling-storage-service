import unittest

from common.entity.find import find


class FindTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_when_dict(self):
        nested_dict = {
            "top": {
                "middle": {"nested": "value"},
                "list": [{"top": {"middle": {"nested": "value 1"}}}, {"top": {"middle": {"nested": "value 2"}}}],
                "intlist": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "4": "anInt",
            }
        }
        self.assertEqual(find(nested_dict, ["top", "middle", "nested"]), "value")
        self.assertEqual(find(nested_dict, ["top", "list", "[0]", "top", "middle", "nested"]), "value 1")
        self.assertEqual(find(nested_dict, ["top", "list", "[1]", "top", "middle", "nested"]), "value 2")
        self.assertEqual(find(nested_dict, ["top", "intlist", [10]]), 11)

        # Validate that a mismatch between object type and key raises a ValueError
        self.assertRaises(ValueError, find, nested_dict, ["top", "[4]"])
        self.assertRaises(ValueError, find, nested_dict, ["top", "4", "[2]"])
        self.assertRaises(ValueError, find, nested_dict, ["top", "list", "top"])

        self.assertRaises(IndexError, find, nested_dict, ["top", "list", "[2]"])
        self.assertRaises(KeyError, find, nested_dict, ["top", "middle", "uknown"])

    def test_when_list(self):
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
        self.assertEqual(find(list_of_nested_dicts, ["[0]", "top", "middle", "nested"]), "value")
        self.assertEqual(
            find(list_of_nested_dicts, ["[0]", "top", "list", "[0]", "top", "middle", "nested"]), "value 1"
        )
        self.assertEqual(
            find(list_of_nested_dicts, ["[0]", "top", "list", "[1]", "top", "middle", "nested"]), "value 2"
        )
        self.assertRaises(IndexError, find, list_of_nested_dicts, ["[2]"])
        self.assertRaises(KeyError, find, list_of_nested_dicts, ["[0]", "top", "middle", "unknown"])
