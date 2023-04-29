import unittest

from common.utils.resolve_reference import (
    AttributeItem,
    IdItem,
    QueryItem,
    _next_reference_part,
    reference_to_reference_items,
)


class ResolveReferenceTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_next_reference_item(self):
        # Example 0
        self.assertEqual(_next_reference_part("$1"), ("$1", None, ""))

        # Example 1
        self.assertEqual(_next_reference_part("/$1"), ("", "/", "$1"))
        self.assertEqual(_next_reference_part("$1"), ("$1", None, ""))

        # Example 2
        self.assertEqual(_next_reference_part("/root/package/$1"), ("", "/", "root/package/$1"))
        self.assertEqual(_next_reference_part("root/package/$1"), ("root", "/", "package/$1"))
        self.assertEqual(_next_reference_part("package/$1"), ("package", "/", "$1"))
        self.assertEqual(_next_reference_part("$1"), ("$1", None, ""))

    def test_reference_with_id_only_to_reference_items(self):
        reference = "$1234-1234-1234"
        items = reference_to_reference_items(reference)
        self.assertEqual(items, [IdItem("1234-1234-1234")])

    def test_reference_with_path_only_to_reference_items(self):
        reference = "/package/subPackage/document"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                QueryItem(query="name=package,isRoot=True"),
                AttributeItem(path="content"),
                QueryItem(query="name=subPackage"),
                AttributeItem(path="content"),
                QueryItem(query="name=document"),
            ],
        )

    def test_reference_with_path_and_simple_attribute_to_reference_items(self):
        reference = "/package/subPackage/document.attribute"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                QueryItem(query="name=package,isRoot=True"),
                AttributeItem(path="content"),
                QueryItem(query="name=subPackage"),
                AttributeItem(path="content"),
                QueryItem(query="name=document"),
                AttributeItem(path="attribute"),
            ],
        )

    def test_reference_with_path_and_list_attribute_to_reference_items(self):
        reference = "/package/subPackage/document.attribute[0]"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                QueryItem(query="name=package,isRoot=True"),
                AttributeItem(path="content"),
                QueryItem(query="name=subPackage"),
                AttributeItem(path="content"),
                QueryItem(query="name=document"),
                AttributeItem(path="attribute"),
                AttributeItem(path="[0]"),
            ],
        )

    def test_reference_with_id_and_list_attribute_to_reference_items(self):
        reference = "/$1.attribute[0]"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                IdItem("1"),
                AttributeItem(path="attribute"),
                AttributeItem(path="[0]"),
            ],
        )

    def test_reference_with_query_to_reference_items(self):
        reference = "/[(_id=1)]"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                QueryItem(query="_id=1"),
            ],
        )

    def test_reference_with_query_and_attribute_query_to_reference_items(self):
        reference = "/[(_id=1)].attribute(key1=value1,key2=value2)"
        items = reference_to_reference_items(reference)
        self.assertEqual(
            items,
            [
                QueryItem(query="_id=1"),
                AttributeItem(path="attribute"),
                QueryItem(query="key1=value1,key2=value2"),
            ],
        )
