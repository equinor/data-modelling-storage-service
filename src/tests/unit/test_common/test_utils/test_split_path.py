import unittest

from common.utils.resolve_address import split_path


class SplitPathTestCase(unittest.TestCase):
    def test_remove_last_reference_part(self):
        path = "$1-2-3.content[1](name=test)(name=test,isRoot=True,yyz=rush)"
        self.assertEqual("$1-2-3.content[1](name=test)", "".join(split_path(path)[:-1]))

    def test_split_complex_reference(self):
        path = "/[(_id=1)].content[(name=myCarRental)].cars[0]"
        path_parts = split_path(path)
        self.assertEqual(["/", "[(_id=1)]", ".content", "[(name=myCarRental)]", ".cars", "[0]"], path_parts)

    def test_split_complex_reference2(self):
        path = "$1-2-3"
        path_parts = split_path(path)
        self.assertEqual(["$1-2-3"], path_parts)

    def test_split_complex_reference3(self):
        path = "/package/subPackage/document"
        path_parts = split_path(path)
        self.assertEqual(["/package", "/subPackage", "/document"], path_parts)

    def test_split_complex_reference4(self):
        path = "/package/subPackage/document.attribute"
        path_parts = split_path(path)
        self.assertEqual(["/package", "/subPackage", "/document", ".attribute"], path_parts)

    def test_split_complex_reference5(self):
        path = "/package/subPackage/document.attribute[0]"
        path_parts = split_path(path)
        self.assertEqual(["/package", "/subPackage", "/document", ".attribute", "[0]"], path_parts)

    def test_split_complex_reference6(self):
        path = "/$1.attribute[0]"
        path_parts = split_path(path)
        self.assertEqual(["/$1", ".attribute", "[0]"], path_parts)

    def test_split_complex_reference7(self):
        path = "/[(_id=1)]"
        path_parts = split_path(path)
        self.assertEqual(["/", "[(_id=1)]"], path_parts)

    def test_split_complex_reference8(self):
        path = "/[(_id=1)].attribute(key1=value1,key2=value2)"
        path_parts = split_path(path)
        self.assertEqual(["/", "[(_id=1)]", ".attribute", "(key1=value1,key2=value2)"], path_parts)
