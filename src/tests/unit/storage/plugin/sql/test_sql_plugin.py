import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker
from src.storage.repositories.plugin.sql import SQLClient  # Import your SQLClient class from your module
from alembic.config import Config
import json
import os
import shutil

study="""{
    "type": "models/signals_simple/Study",
    "cases": [
       {
          "name": "case1",
          "type": "models/signals_simple/Case",
          "description": "",
          "newAttribute": 32,
          "duration": 100,
          "timeStep": 0.1,
          "components": [
             {
                "type": "models/signals_simple/SinComp",
                "A": 10,
                "T": 10,
                "phase": 0.1
             }
         
          ],
          "signal": {
             "name": "signal",
             "type": "models/containers/EquallySpacedSignal",
             "value": [1, 2, 3, 4, 99, 6, 7, 1, 2, 3, 4, 5, 1, 2 ,3, 4, 9],
             "xname": "time",
             "xunit": "s",
             "xdelta": 0.1,
             "xstart": 0,
             "xlabel": "Time",
             "label": " ",
             "legend": " ",
             "unit": "m"
          }
       }
    ]
}"""


study2="""{
    "type": "models/signals_simple/Study",
    "cases": [
       {
          "name": "case1",
          "type": "models/signals_simple/Case",
          "description": "",
          "newAttribute": 32,
          "duration": 100,
          "timeStep": 0.1,
          "components": [
             {
                "type": "models/signals_simple/SinComp",
                "A": 10,
                "T": 10,
                "phase": 0.1
             },
             {
                "type": "models/signals_simple/SinComp",
                "A": 2,
                "T": 2,
                "phase": 0
             },
             {
                "type": "models/signals_simple/SinComp",
                "A": 100,
                "T": 20,
                "phase": 0.05
             }
          ],
          "signal": {
             "name": "signal",
             "type": "models/containers/EquallySpacedSignal",
             "value": [1, 2, 3, 4, 99, 6, 7, 1, 2, 3, 4, 5, 1, 2 ,3, 4, 9],
             "xname": "time",
             "xunit": "s",
             "xdelta": 0.1,
             "xstart": 0,
             "xlabel": "Time",
             "label": " ",
             "legend": " ",
             "unit": "m"
          }
       }
    ]
}"""
study=json.loads(study)
study2=json.loads(study2)

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
class TestSQLClient(unittest.TestCase):
    @patch('src.storage.repositories.plugin.sql.sql.sessionmaker')
    @patch('src.storage.repositories.plugin.sql.models.blueprint_handling.default_blueprint_provider.get_blueprint')
    @patch('src.storage.repositories.plugin.sql.sql.default_blueprint_provider.get_blueprint')
    def test_setUp(self, mock_sessionmaker,mock_get_blueprint_model, mock_get_blueprint, ):        # Mock the SQLAlchemy components
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

        folder_path=os.path.dirname(__file__)
        alembic_versions_path = os.path.join(folder_path, "alembic2", "versions")

        for filename in os.listdir(alembic_versions_path):
            file_path = os.path.join(alembic_versions_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        mock_get_blueprint.side_effect = side_effect
        mock_get_blueprint_model.side_effect = side_effect

        engine = create_engine(r'postgresql://postgres:postgres@localhost/mydatabase')
        meta = MetaData()
        meta.reflect(bind=engine)
        meta.drop_all(bind=engine)
        Session = sessionmaker(bind=engine)()
        session = Session
        mock_sessionmaker.return_value = Session


        client = SQLClient(engine=engine)
        conf_path= os.path.join(folder_path,'alembic.ini')

        client.alembic_cfg= Config(conf_path)

        # Mock metadata
        # Bind a session to the engine
        # Perform the add_table method and assert

        result = client.add_table("dmss://system/models/signals_simple/Study")

        reflected_metadata = MetaData()
        reflected_metadata.reflect(bind=engine)
        self.assertTrue(result)
        client.add_insert(entity=study2,id='255127f8-4a84-4ab8-bdd2-d0e930e42bb6')
        entity=client.get(id='255127f8-4a84-4ab8-bdd2-d0e930e42bb6')
        assert len(entity['cases'])==len(study2['cases'])
        client.update(id='255127f8-4a84-4ab8-bdd2-d0e930e42bb6',entity=study)
        entity2=client.get(id='255127f8-4a84-4ab8-bdd2-d0e930e42bb6')
        assert len(entity['cases'][0]['components']) != len(entity2['cases'][0]['components'])
        client.delete(id='255127f8-4a84-4ab8-bdd2-d0e930e42bb6')
        entity3=client.get('255127f8-4a84-4ab8-bdd2-d0e930e42bb6')
        assert entity3 != entity2
        assert entity3=="Could not find id:255127f8-4a84-4ab8-bdd2-d0e930e42bb6 in database"


if __name__ == '__main__':
    unittest.main()