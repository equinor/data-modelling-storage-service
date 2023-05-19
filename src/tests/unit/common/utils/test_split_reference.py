import unittest

from common.utils.resolve_reference import split_reference


class SplitReferenceTestCase(unittest.TestCase):
    def test_remove_last_reference_part(self):
        reference = "$123-65435634-123.content[1](name=test)(name=test,isRoot=True,yyz=rush)"
        self.assertEqual("$123-65435634-123.content[1](name=test)", "".join(split_reference(reference)[:-1]))

    def test_split_complex_reference(self):
        reference = "/[(_id=1)].content[(name=myCarRental)].cars[0]"
        ref_pars = split_reference(reference)
        self.assertEqual(["/", "[(_id=1)]", ".content", "[(name=myCarRental)]", ".cars", "[0]"], ref_pars)

    def test_split_complex_reference2(self):
        reference = "$1234-1234-1234"
        ref_pars = split_reference(reference)
        self.assertEqual(["$1234-1234-1234"], ref_pars)

    def test_split_complex_reference3(self):
        reference = "/package/subPackage/document"
        ref_pars = split_reference(reference)
        self.assertEqual(["/package", "/subPackage", "/document"], ref_pars)

    def test_split_complex_reference4(self):
        reference = "/package/subPackage/document.attribute"
        ref_pars = split_reference(reference)
        self.assertEqual(["/package", "/subPackage", "/document", ".attribute"], ref_pars)

    def test_split_complex_reference5(self):
        reference = "/package/subPackage/document.attribute[0]"
        ref_pars = split_reference(reference)
        self.assertEqual(["/package", "/subPackage", "/document", ".attribute", "[0]"], ref_pars)

    def test_split_complex_reference6(self):
        reference = "/$1.attribute[0]"
        ref_pars = split_reference(reference)
        self.assertEqual(["/$1", ".attribute", "[0]"], ref_pars)

    def test_split_complex_reference7(self):
        reference = "/[(_id=1)]"
        ref_pars = split_reference(reference)
        self.assertEqual(["/", "[(_id=1)]"], ref_pars)

    def test_split_complex_reference8(self):
        reference = "/[(_id=1)].attribute(key1=value1,key2=value2)"
        ref_pars = split_reference(reference)
        self.assertEqual(["/", "[(_id=1)]", ".attribute", "(key1=value1,key2=value2)"], ref_pars)
