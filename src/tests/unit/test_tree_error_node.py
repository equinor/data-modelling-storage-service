import unittest
from unittest import skip

from domain_classes.dto import DTO
from domain_classes.tree_node import Node


all_contained_cases_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint1",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
    ],
    "storageRecipes": [],
    "uiRecipes": [],
}


class ErrorTreenodeTestCase(unittest.TestCase):

    # error node breaks tests in document service.
    # add uncommented line in tree_node from_dict to enable this test.
    @skip
    def test_error_node_renamed(self):
        document_1 = {
            "uid": "1",
            "name": "Parent",
            "description": "",
            "type": "all_contained_cases_blueprint",
            # renamed nested to nested2
            "nested2": {"name": "Nested 1", "description": "", "type": "basic_blueprint"},
            "_blueprint": all_contained_cases_blueprint,
        }

        class BlueprintProvider:
            def get_blueprint(type: str):
                raise Exception("fix me")

        root = Node.from_dict(DTO(document_1), BlueprintProvider())
        error_msg = root.children[0].error_message
        assert error_msg is not None
