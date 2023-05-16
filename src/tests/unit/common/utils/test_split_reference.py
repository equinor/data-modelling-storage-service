import unittest

from common.utils.resolve_reference import split_reference


class SplitReferenceTestCase(unittest.TestCase):
    def test_remove_last_reference_part(self):
        reference = "$123-65435634-123.content[1](name=test)(name=test,isRoot=True,yyz=rush)"
        self.assertEqual("$123-65435634-123.content[1](name=test)", "".join(split_reference(reference)[:-1]))
