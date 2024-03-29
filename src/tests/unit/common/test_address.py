import unittest

from common.address import Address
from common.exceptions import ApplicationException


class AddressTestCase(unittest.TestCase):
    def test_init(self):
        addr = Address(path="a", data_source="b")

        self.assertEqual(addr.path, "a")
        self.assertEqual(addr.data_source, "b")
        self.assertEqual(addr.protocol, "dmss")

    def test_init_with_other_protocol_than_dmss_throws_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Address(path="a", data_source="b", protocol="x")

    def test_from_absolute_with_protocol(self):
        path = "dmss://ds/b/$c123.A"

        addr = Address.from_absolute(path)

        self.assertEqual(addr.protocol, "dmss")
        self.assertEqual(addr.data_source, "ds")
        self.assertEqual(addr.path, "b/$c123.A")

    def test_from_absolute_without_protocol(self):
        path = "ds/b/$c123.A"

        addr = Address.from_absolute(path)

        self.assertEqual(addr.protocol, "dmss")
        self.assertEqual(addr.data_source, "ds")
        self.assertEqual(addr.path, "b/$c123.A")

    def test_from_relative_where_path_is_absolute_returns_valid_path(self):
        path = "dmss://ds/example/$123.A"

        addr = Address.from_relative(path, None, "ds")

        self.assertEqual(addr.protocol, "dmss")
        self.assertEqual(addr.data_source, "ds")
        self.assertEqual(addr.path, "example/$123.A")

    def test_from_relative_where_path_is_absolute_without_protocol_returns_valid_path(self):
        path = "example/$123.A"

        addr = Address.from_relative(path, None, "ds")

        self.assertEqual(addr.protocol, "dmss")
        self.assertEqual(addr.data_source, "ds")
        self.assertEqual(addr.path, "example/$123.A")

    def test_from_relative_replaces_hat_with_document_id(self):
        path = "^example/$123.A"

        addr = Address.from_relative(path, "doc_id/", data_source="ds")

        self.assertEqual(addr.protocol, "dmss")
        self.assertEqual(addr.data_source, "ds")
        self.assertEqual(addr.path, "$doc_id/example/$123.A")

    def test_from_relative_without_document_id_throws_ApplicationException(self):
        path = "^example/$123.A"

        with self.assertRaises(ApplicationException):
            Address.from_relative(path, None, data_source="ds")

    def test_one_attribute_up_from_current_document_with_relative_path(self):
        address = "~.data"
        relative_path = ["attribute[1]", "attribute_b"]
        document_id = "doc_id"
        addr = Address.from_relative(address, document_id, data_source="ds", relative_path=relative_path)

        self.assertEqual(addr.path, "$doc_id.attribute[1].data")

    def test_two_attributes_up_from_current_document_with_relative_path(self):
        address = "~.~.data"
        relative_path = ["attribute_a", "attribute_b"]
        document_id = "doc_id"
        addr = Address.from_relative(address, document_id, data_source="ds", relative_path=relative_path)

        self.assertEqual(addr.path, "$doc_id.data")

    def test_two_attributes_up_from_current_document_without_relative_path_throws_ApplicationException(self):
        address = "~.~.data"
        document_id = "doc_id"
        with self.assertRaises(ApplicationException):
            Address.from_relative(address, document_id, data_source="ds")

    def test_go_up_from_current_document_more_than_possible_throws_ApplicationException(self):
        address = "~.~.~.~.data"
        relative_path = ["attribute_a", "attribute_b"]
        document_id = "doc_id"
        with self.assertRaises(ApplicationException):
            Address.from_relative(address, document_id, data_source="ds", relative_path=relative_path)
