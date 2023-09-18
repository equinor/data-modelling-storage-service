import unittest

from common.utils.data_structure.dot_notation import to_dot_notation


class DotNotationTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_to_dot_notation_when_dict(self):
        path = ["top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "top.middle.nested")

    def test_to_dot_notation_when_list(self):
        path = ["[0]", "top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "[0].top.middle.nested")

    def test_to_dot_notation_when_nested_list(self):
        path = ["top", "list", "[0]", "top", "middle", "nested"]
        self.assertEqual(to_dot_notation(path), "top.list[0].top.middle.nested")
