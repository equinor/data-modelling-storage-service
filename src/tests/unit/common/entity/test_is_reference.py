import unittest

import enums
from common.entity.is_reference import is_reference


class TestIsReference(unittest.TestCase):
    def test_is_reference_true(self):
        entity = {"type": enums.SIMOS.REFERENCE.value}
        self.assertTrue(is_reference(entity))

    def test_is_reference_false(self):
        entity = {"type": "NotAReference"}
        self.assertFalse(is_reference(entity))

    def test_is_reference_not_dict(self):
        entity = "not_a_dict"
        self.assertFalse(is_reference(entity))


if __name__ == "__main__":
    unittest.main()
