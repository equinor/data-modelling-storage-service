import unittest

from common.utils.data_structure.compare import get_and_print_diff
from features.export.use_cases.export_meta_use_case import concat_meta_data


class ConcatMetaTestCase(unittest.TestCase):
    def test_concat_entity(self):
        existing_meta = {
            "type": "CORE:Meta",
            "version": "0.0.1",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "CORE",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
            ],
        }
        new_meta = {
            "type": "CORE:Meta",
            "version": "0.0.1",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "TEST-MODELS",
                    "address": "DemoApplicationDataSource/models",
                    "version": "0.0.1",
                    "protocol": "dmss",
                }
            ],
        }

        concat_meta = concat_meta_data(existing_meta, new_meta)
        expected = {
            "type": "CORE:Meta",
            "version": "0.0.1",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "CORE",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "TEST-MODELS",
                    "address": "DemoApplicationDataSource/models",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
            ],
        }

        result = get_and_print_diff(concat_meta, expected)
        self.assertEqual(result, [])

    def test_concat_entity_with_override(self):
        existing_meta = {
            "type": "CORE:Meta",
            "version": "0.0.1",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "CORE",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "EXISTING-ALIAS",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
            ],
        }
        new_meta = {
            "type": "dmss://system/SIMOS/Meta",
            "version": "3.3.3",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "EXISTING-ALIAS",
                    "address": "an/address",
                    "version": "2.2.2",
                    "protocol": "http",
                }
            ],
        }

        concat_meta = concat_meta_data(existing_meta, new_meta)
        expected = {
            "type": "dmss://system/SIMOS/Meta",
            "version": "3.3.3",
            "dependencies": [
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "CORE",
                    "address": "system/SIMOS",
                    "version": "0.0.1",
                    "protocol": "dmss",
                },
                {
                    "type": "dmss://system/SIMOS/Dependency",
                    "alias": "EXISTING-ALIAS",
                    "address": "an/address",
                    "version": "2.2.2",
                    "protocol": "http",
                },
            ],
        }

        result = get_and_print_diff(concat_meta, expected)
        self.assertEqual(result, [])
