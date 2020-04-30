import unittest

from api.classes.blueprint import Blueprint
from api.classes.dimension import Dimension
from api.classes.dto import DTO
from api.core.repository.file import TemplateRepositoryFromFile
from api.core.use_case.utils.build_complex_search import build_mongo_query
from api.core.use_case.utils.create_entity import CreateEntity
from api.utils.helper_functions import schemas_location


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


class BlueprintProvider:
    def get_blueprint(self, template_type: str):
        if template_type == "basic_blueprint":
            return Blueprint(DTO(basic_blueprint))
        elif template_type == "test/Nested":
            return Blueprint(DTO(nested_blueprint))


blueprint_provider = BlueprintProvider()


class DefaultArrayTestCase(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
