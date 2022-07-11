import unittest

from domain_classes.blueprint import Blueprint

from utils.build_complex_search import build_mongo_query

basic_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "A box",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "integer", "type": "system/SIMOS/BlueprintAttribute", "name": "length"},
    ],
}
nested_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Nested",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "integer", "type": "system/SIMOS/BlueprintAttribute", "name": "an_int"},
        {"attributeType": "test/Nested", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
    ],
}

nested_blueprint_w_list = {
    "type": "system/SIMOS/Blueprint",
    "name": "NestedList",
    "description": "Third blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "integer", "type": "system/SIMOS/BlueprintAttribute", "name": "length", "dimensions": "3"},
        {
            "attributeType": "NestedList",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "nestedList",
            "dimensions": "3",
        },
    ],
}


class BlueprintProvider:
    def get_blueprint(self, template_type: str):
        if template_type == "basic_blueprint":
            return Blueprint(basic_blueprint)
        elif template_type == "test/Nested":
            return Blueprint(nested_blueprint)
        elif template_type == "NestedList":
            return Blueprint(nested_blueprint_w_list)


blueprint_provider = BlueprintProvider()


class CreateSearchQueryTestCase(unittest.TestCase):
    def test_simple_search_query(self):
        search_data = {"type": "basic_blueprint", "name": "whatever"}
        query = build_mongo_query(blueprint_provider.get_blueprint, search_data)

        assert query == {"type": "basic_blueprint", "name": {"$regex": ".*whatever.*", "$options": "i"}}

    def test_nested_search_query(self):
        search_data = {
            "type": "test/Nested",
            "name": "whatever",
            "nested": {"nested": {"name": "whatever", "an_int": "<100"}},
        }
        query = build_mongo_query(blueprint_provider.get_blueprint, search_data)

        assert query == {
            "type": "test/Nested",
            "name": {"$regex": ".*whatever.*", "$options": "i"},
            "nested.type": "test/Nested",
            "nested.nested.type": "test/Nested",
            "nested.nested.name": {"$regex": ".*whatever.*", "$options": "i"},
            "nested.nested.an_int": {"$lt": 100.0},
        }

    def test_nested_list_search_query(self):
        search_data = {
            "type": "NestedList",
            "name": "first_level",
            "nestedList": [{"name": "second_level", "nestedList": [{"name": "third_level", "length": ["<100"]}]}],
        }
        query = build_mongo_query(blueprint_provider.get_blueprint, search_data)

        assert query == {
            "type": "NestedList",
            "name": {"$regex": ".*first_level.*", "$options": "i"},
            "nestedList.type": "NestedList",
            "nestedList.name": {"$regex": ".*second_level.*", "$options": "i"},
            "nestedList.nestedList.type": "NestedList",
            "nestedList.nestedList.name": {"$regex": ".*third_level.*", "$options": "i"},
            "nestedList.nestedList.length": {"$lt": 100.0},
        }


if __name__ == "__main__":
    unittest.main()
