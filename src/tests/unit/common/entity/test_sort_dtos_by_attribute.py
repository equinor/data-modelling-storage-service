import unittest

from features.search.use_cases.search_use_case.sort_dtos_by_attribute import (
    sort_dtos_by_attribute,
)


class TestSortDTOsByAttribute(unittest.TestCase):
    def test_sort_by_single_attribute(self):
        data = [{"age": 21}, {"age": 40}, {"age": 18}]
        sorted_data = sort_dtos_by_attribute(data, "age")
        self.assertEqual(sorted_data, [{"age": 18}, {"age": 21}, {"age": 40}])

    def test_sort_by_nested_attribute(self):
        data = [{"info": {"age": 21}}, {"info": {"age": 40}}, {"info": {"age": 18}}]
        sorted_data = sort_dtos_by_attribute(data, "info.age")
        self.assertEqual(sorted_data, [{"info": {"age": 18}}, {"info": {"age": 21}}, {"info": {"age": 40}}])

    def test_sort_by_parent_attribute_raises_TypeError(self):
        data = [{"info": {"age": 21}}, {"info": {"age": 40}}, {"info": {"age": 18}}]
        with self.assertRaises(TypeError):
            # Can't compare dict with dict
            sorted_data = sort_dtos_by_attribute(data, "info")

    def test_empty_list(self):
        data: list[dict] = []
        sorted_data = sort_dtos_by_attribute(data, "age")
        self.assertEqual(sorted_data, [])

    def test_invalid_attribute_raises_KeyError(self):
        data = [{"age": 21}, {"age": 40}, {"age": 18}]
        with self.assertRaises(KeyError):
            sort_dtos_by_attribute(data, "invalid_attribute")

    def test_incomparable_data_types_raises_TypeError(self):
        data = [{"age": "21"}, {"age": 40}, {"age": 18}]
        with self.assertRaises(TypeError):
            # raises TypeError because can't compare "str" and "int"
            sort_dtos_by_attribute(data, "age")

    # Add more test cases as you find necessary


if __name__ == "__main__":
    unittest.main()
