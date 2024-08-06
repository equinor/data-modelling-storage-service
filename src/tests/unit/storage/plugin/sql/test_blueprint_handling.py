import unittest
from unittest.mock import patch, MagicMock
from src.storage.repositories.plugin.sql.models.blueprint_handling import SQLBlueprint, resolve_model

example_bp1 = {
    "name": "Case",
    "type": "dmss://system/SIMOS/Blueprint",
    "description": "",
    "extends": [
        "dmss://system/SIMOS/NamedEntity"
    ],
    "attributes": [
        {
            "name": "name",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
        },
        {
            "name": "type",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
        },
        {
            "name": "description",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
        },
        {
            "name": "duration",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "number"
        },
        {
            "name": "newAttribute",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "number"
        },
        {
            "name": "timeStep",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "number"
        },
        {
            "name": "components",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "./SinComp",
            "dimensions": "*"
        },
        {
            "name": "signal",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "../containers/EquallySpacedSignal",
            "dimensions": "*"
        }
    ]
}

example_bp4={
  "name": "EquallySpacedSignal",
  "type": "dmss://system/SIMOS/Blueprint",
  "description": "data model for an equally spaced signal.",
  "attributes": [
    {
      "name": "type",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "string"
    },
    {
      "name": "name",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "variable name for named accessing",
      "attributeType": "string",
      "default": "signal",
      "contained": True,
      "optional": False
    },
    {
      "name": "description",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "instance description",
      "attributeType": "string",
      "default": "signal desc",
      "contained": True,
      "optional": True
    },
    {
      "name": "value",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "data points.",
      "attributeType": "number",
      "dimensions": "*",
      "contained": True,
      "optional": False
    },
    {
      "name": "xname",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "name for the x value",
      "attributeType": "string",
      "contained": True,
      "optional": True
    },
    {
      "name": "xdescription",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "description for the x-axis",
      "attributeType": "string",
      "contained": True,
      "optional": True
    },
    {
      "name": "xunit",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "x-axis unit.",
      "attributeType": "string",
      "default": "s",
      "contained": True,
      "optional": True
    },
    {
      "name": "xdelta",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "x-axis or index spacing.",
      "attributeType": "number",
      "contained": True,
      "default": 1,
      "optional": False
    },
    {
      "name": "xstart",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "x-axis or index start.",
      "attributeType": "number",
      "contained": True,
      "default": 0,
      "optional": True
    },
    {
      "name": "xlabel",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "label for the x-axis.",
      "attributeType": "string",
      "default": "time",
      "contained": True,
      "optional": False
    },
    {
      "name": "label",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "label for the y-axis.",
      "attributeType": "string",
      "default": " ",
      "contained": True,
      "optional": False
    },
    {
      "name": "legend",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "description of xy values to be used as legend.",
      "attributeType": "string",
      "default": " ",
      "contained": True,
      "optional": False
    },
    {
      "name": "unit",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "description": "data unit.",
      "attributeType": "string",
      "default": "m",
      "contained": True,
      "optional": False
    }
  ]
}
example_bp2={
  "name": "Study",
  "type": "dmss://system/SIMOS/Blueprint",
  "description": "",
  "attributes": [
    {
      "name": "type",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "string"
    },
    {
      "name": "cases",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "label": "Cases",
      "attributeType": "./Case",
      "dimensions": "*",
      "contained": True
    }
  ]
}
example_bp3={
  "name": "SinComp",
  "type": "dmss://system/SIMOS/Blueprint",
  "description": "",
  "attributes": [
    {
      "name": "type",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "string"
    },
    {
      "name": "A",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "number",
      "default": 0,
      "optional": False
    },
    {
      "name": "T",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "number",
      "default": 0,
      "optional": False
    },
    {
      "name": "phase",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "number",
      "optional": False
    },
    {
      "name": "signal",
      "type": "dmss://system/SIMOS/BlueprintAttribute",
      "attributeType": "../containers/EquallySpacedSignal"
    }
  ]
}

class TestSQLBlueprint(unittest.TestCase):
    def test_from_dict(self):
        # Instantiate SQLBlueprint with required fields
        obj = SQLBlueprint.from_dict(example_bp1)

        # Call the method
        obj.from_dict(example_bp1)

        # Verify that the blueprint was correctly loaded
        self.assertEqual(obj.name, 'Case')
        self.assertEqual(obj.type, 'dmss://system/SIMOS/Blueprint')
        self.assertEqual(obj.description, '')
        self.assertEqual(len(obj.attributes), len(example_bp1['attributes']))

    @patch('src.storage.repositories.plugin.sql.models.blueprint_handling.default_blueprint_provider.get_blueprint')
    def test_generate_models_m2m_rel(self, mock_get_blueprint_sql):
        def side_effect(address):
            mock_blueprint = MagicMock()
            if address == "dmss://system/models/signals_simple/Case":
                mock_blueprint.to_dict.return_value = example_bp1
            elif address == "dmss://system/models/signals_simple/Study":
                mock_blueprint.to_dict.return_value = example_bp2
            elif address == "dmss://system/models/signals_simple/SinComp":
                mock_blueprint.to_dict.return_value = example_bp3
            elif address == "dmss://system/models/containers/EquallySpacedSignal":
                mock_blueprint.to_dict.return_value = example_bp4
            return mock_blueprint

        mock_get_blueprint_sql.side_effect = side_effect
        obj = SQLBlueprint.from_dict(example_bp2)
        obj.from_dict(example_bp1)
        obj.path = 'dmss://system/models/signals_simple/Study'
        model=resolve_model(obj)
        tables=len(model.metadata.sorted_tables)
        assert tables == 9
        assert model.metadata.sorted_tables[0].fullname=='Case'
        assert model.metadata.sorted_tables[8].fullname == 'Study_Case_map'



if __name__ == '__main__':
    unittest.main()