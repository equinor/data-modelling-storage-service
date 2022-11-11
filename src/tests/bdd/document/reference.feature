Feature: Add and remove references

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

  Scenario: Insert and remove reference (in list)
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "sys://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

    Given there exist document with id "3f9ff99f-9cb5-4afc-947b-a3224eee341f" in data source "test-DS"
    """
    {
      "type": "sys://system/SIMOS/Blueprint",
      "name": "some-blueprint",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """
    Given i access the resource url "/api/v1/reference/test-DS/1.content"
    When i make a "PUT" request
    """
    {
      "name": "some-blueprint",
      "type": "sys://system/SIMOS/Blueprint",
      "_id": "3f9ff99f-9cb5-4afc-947b-a3224eee341f"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "TestData",
      "description": "",
      "type": "sys://system/SIMOS/Package",
      "content": [
        {
          "name": "some-blueprint",
          "type": "sys://system/SIMOS/Blueprint",
          "_id": "3f9ff99f-9cb5-4afc-947b-a3224eee341f"
        }
    ],
      "isRoot": true
    }
    """
    Given i access the resource url "/api/v1/reference/test-DS/1.content.0"
    When i make a "DELETE" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "TestData",
      "description": "",
      "type": "sys://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

  Scenario: Insert and remove reference (simple)
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "sys://system/SIMOS/Package",
      "content": [
        {
          "name": "Turbine",
          "type": "sys://system/SIMOS/Blueprint",
          "_id": "2"
        },
        {
          "name": "Mooring",
          "type": "sys://system/SIMOS/Blueprint",
          "_id": "3"
        },
        {
          "name": "myTurbine",
          "type": "sys://system/SIMOS/Blueprint",
          "_id": "4"
        },
        {
          "name": "myMooring",
          "type": "sys://system/SIMOS/Blueprint",
          "_id": "3f9ff99f-9cb5-4afc-947b-a3224eee341f"
        }
      ],
      "isRoot": true
    }
    """

    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "name": "Turbine",
      "type": "sys://system/SIMOS/Blueprint",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "description": "",
      "attributes": [
        {
          "name": "Mooring",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "attributeType": "sys://test-DS/TestData/Mooring",
          "optional": true,
          "contained": false
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
      "name": "Mooring",
      "type": "sys://system/SIMOS/Blueprint",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "description": "",
      "attributes": [
        {
          "name": "Bigness",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "description": "How big? Very",
          "attributeType": "integer",
          "default": "",
          "contained": true
        }
      ]
    }
    """
    Given there exist document with id "4" in data source "test-DS"
    """
    {
      "name": "myTurbine",
      "type": "sys://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships",
      "Mooring": {}
    }
    """
    Given there exist document with id "3f9ff99f-9cb5-4afc-947b-a3224eee341f" in data source "test-DS"
    """
    {
    "name": "myMooring",
    "type": "sys://test-DS/TestData/Mooring",
    "description": "",
    "Bigness": 10
    }
    """
    Given i access the resource url "/api/v1/reference/test-DS/4.Mooring"
    When i make a "PUT" request
    """
    {
      "name": "myMooring",
      "type": "sys://test-DS/TestData/Mooring",
      "_id": "3f9ff99f-9cb5-4afc-947b-a3224eee341f"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myTurbine",
      "type": "sys://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships",
      "Mooring": {
        "name": "myMooring",
        "type": "sys://test-DS/TestData/Mooring",
        "_id": "3f9ff99f-9cb5-4afc-947b-a3224eee341f"
      }
    }
    """
    Given i access the resource url "/api/v1/reference/test-DS/4.Mooring"
    When i make a "DELETE" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myTurbine",
      "type": "sys://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships",
      "Mooring": {}
    }
    """
