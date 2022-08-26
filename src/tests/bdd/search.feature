Feature: Explorer - Search entity

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name         |
      | entities     |
      | moreEntities |
      | blueprints   |

    Given there are repositories in the data sources
      | data-source    | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | entities       | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | entities     | mongo-db | default   |
      | moreEntities   | db   | 27017 | maf      | maf      | false | repo2     |  bdd-test    | moreEntities | mongo-db | default   |
      | blueprints     | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | blueprints   | mongo-db | default   |

    Given there exist document with id "1" in data source "blueprints"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "2",
                "name": "ValuesBlueprint",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "3",
                "name": "NestedVectorsBlueprint",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "4",
                "name": "NestedBlueprint",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "5",
                "name": "NestedListBlueprint",
                "type": "system/SIMOS/Blueprint"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "blueprints"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "ValuesBlueprint",
      "description": "This describes a blueprint that has a few different primitive attributes",
      "attributes": [
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "name",
          "attributeType": "string",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "description",
          "attributeType": "string",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type",
          "attributeType": "string",
          "default": "blueprints/root_package/ValuesBlueprint",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "a_number",
          "attributeType": "number",
          "default": "120",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "an_integer",
          "attributeType": "integer",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "a_string",
          "attributeType": "string",
          "optional": false
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "blueprints"
    """
    {
      "name": "NestedVectorsBlueprint",
      "type": "system/SIMOS/Blueprint",
      "description": "This describes a blueprint that has two attributes",
      "attributes": [
        {
          "name": "height",
          "type": "system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "label": "height",
          "default": "100.0",
          "contained": "true"
        },
        {
          "name": "width",
          "type": "system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "label": "width",
          "default": "100.0",
          "contained": "true"
        }
      ]
    }
    """

    Given there exist document with id "4" in data source "blueprints"
    """
    {
      "name": "NestedBlueprint",
      "type": "system/SIMOS/Blueprint",
      "description": "This describes a blueprint that has another blueprint as one of its attributes",
      "attributes": [
        {
          "name": "Vectors",
          "type": "system/SIMOS/BlueprintAttribute",
          "attributeType": "blueprints/root_package/NestedVectorsBlueprint",
          "label": "Vectors",
          "contained": true
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "blueprints"
    """
    {
      "name": "NestedListBlueprint",
      "type": "system/SIMOS/Blueprint",
      "description": "This describes a blueprint that contains a list of nested entities",
      "attributes": [
        {
          "name": "VectorList",
          "type": "system/SIMOS/BlueprintAttribute",
          "attributeType": "blueprints/root_package/NestedVectorsBlueprint",
          "dimensions": "*",
          "contained": true
        }
      ]
    }
    """

    Given there exist document with id "1" in data source "entities"
    """
    {
      "name": "primitive_1",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 120.0,
      "an_integer": 5,
      "a_string": "abc"
    }
    """

    Given there exist document with id "99" in data source "moreEntities"
    """
    {
      "name": "primitive_more",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 10.0,
      "an_integer": 10,
      "a_string": "def"
    }
    """

    Given there exist document with id "2" in data source "entities"
    """
    {
      "name": "primitive_2",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 150.1,
      "an_integer": 10,
      "a_string": "def"
    }
    """

    Given there exist document with id "3" in data source "entities"
    """
    {
      "name": "nestedVectors_1",
      "description": "Some nested vectors",
      "type": "blueprints/root_package/NestedBlueprint",
      "Vectors": {
        "name": "Vectors",
        "type": "blueprints/root_package/NestedVectorsBlueprint",
        "height": 223.3,
        "width": 133.7
      }
    }
    """

    Given there exist document with id "4" in data source "entities"
    """
    {
      "name": "nestedVectors_2",
      "description": "Some other nested vectors",
      "type": "blueprints/root_package/NestedBlueprint",
      "Vectors": {
        "name": "Vectors",
        "type": "blueprints/root_package/NestedVectorsBlueprint",
        "height": 64.3,
        "width": 512.1
      }
    }
    """

    Given there exist document with id "5" in data source "entities"
    """
    {
      "name": "myNestedListEntity_1",
      "description": "Some entity with a list of items",
      "type": "blueprints/root_package/NestedListBlueprint",
      "VectorList": [
        {
          "name": "Vector_1",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 64.3,
          "width": 512.1
        },
        {
          "name": "Vector_2",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 280.1,
          "width": 123.4
        }
      ]
    }
    """


  Scenario: Search with primitive filter, all hit
    Given i access the resource url "/api/v1/search?data_sources=entities"
    When i make a "POST" request
    """
    {
      "name": "PrImiT",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": ">100",
      "an_integer": "<11"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/2": {
        "_id": "2",
        "name": "primitive_2",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 150.1,
        "an_integer": 10,
        "a_string": "def"
      },
      "entities/1": {
        "_id": "1",
        "name": "primitive_1",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 120.0,
        "an_integer": 5,
        "a_string": "abc"
      }
    }
    """
  Scenario: Search with primitive filter, 1 hit
    Given i access the resource url "/api/v1/search?data_sources=entities"
    When i make a "POST" request
    """
    {
      "name": "PrImiT",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": ">121",
      "an_integer": ">5",
      "a_string": "de"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/2": {
        "_id": "2",
        "name": "primitive_2",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 150.1,
        "an_integer": 10,
        "a_string": "def"
      }
    }
    """

  Scenario: Search with sorting by attribute, top level attribute
    Given i access the resource url "/api/v1/search?data_sources=entities&sort_by_attribute=a_number"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/ValuesBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/1": {
        "_id": "1",
        "name": "primitive_1",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 120.0,
        "an_integer": 5,
        "a_string": "abc"
      },
      "entities/2": {
        "_id": "2",
        "name": "primitive_2",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 150.1,
        "an_integer": 10,
        "a_string": "def"
      }
    }
    """

  Scenario: Search with sorting by default sort_by_attribute, name
    Given i access the resource url "/api/v1/search?data_sources=entities"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/NestedBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/3": {
        "_id": "3",
        "name": "nestedVectors_1",
        "description": "Some nested vectors",
        "type": "blueprints/root_package/NestedBlueprint",
        "Vectors": {
          "name": "Vectors",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 223.3,
          "width": 133.7
        }
      },
      "entities/4": {
        "_id": "4",
        "name": "nestedVectors_2",
        "description": "Some other nested vectors",
        "type": "blueprints/root_package/NestedBlueprint",
        "Vectors": {
          "name": "Vectors",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 64.3,
          "width": 512.1
        }
      }
    }
    """

  Scenario: Search with sorting by attribute, nested attribute, i.e. sub-attribute
    Given i access the resource url "/api/v1/search?data_sources=entities&sort_by_attribute=Vectors.height"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/NestedBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/4": {
        "_id": "4",
        "name": "nestedVectors_2",
        "description": "Some other nested vectors",
        "type": "blueprints/root_package/NestedBlueprint",
        "Vectors": {
          "name": "Vectors",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 64.3,
          "width": 512.1
        }
      },
      "entities/3": {
        "_id": "3",
        "name": "nestedVectors_1",
        "description": "Some nested vectors",
        "type": "blueprints/root_package/NestedBlueprint",
        "Vectors": {
          "name": "Vectors",
          "type": "blueprints/root_package/NestedVectorsBlueprint",
          "height": 223.3,
          "width": 133.7
        }
      }
    }
    """

  Scenario: Search with sorting by attribute, nested attribute from list by index
    Given i access the resource url "/api/v1/search?data_sources=entities&sort_by_attribute=VectorList.0.width"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/NestedListBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/5": {
        "_id": "5",
        "name": "myNestedListEntity_1",
        "description": "Some entity with a list of items",
        "type": "blueprints/root_package/NestedListBlueprint",
        "VectorList": [
          {
            "name": "Vector_1",
            "type": "blueprints/root_package/NestedVectorsBlueprint",
            "height": 64.3,
            "width": 512.1
          },
          {
            "name": "Vector_2",
            "type": "blueprints/root_package/NestedVectorsBlueprint",
            "height": 280.1,
            "width": 123.4
          }
        ]
      }
    }
    """


    Scenario: Search two data sources for document of type ValuesBlueprint
    Given i access the resource url "/api/v1/search?data_sources=entities&?&data_sources=moreEntities"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/ValuesBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/1":     {
      "_id": "1",
      "name": "primitive_1",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 120.0,
      "an_integer": 5,
      "a_string": "abc"
    },
    "entities/2":     {
      "_id": "2",
      "name": "primitive_2",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 150.1,
      "an_integer": 10,
      "a_string": "def"
    },
    "moreEntities/99": {
      "_id": "99",
      "name": "primitive_more",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 10.0,
      "an_integer": 10,
      "a_string": "def"
      }
    }
    """

  Scenario: Search when one data source does not exist
    Given i access the resource url "/api/v1/search?data_sources=entities&?&data_sources=DOESNOTEXIST"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/ValuesBlueprint"
    }
    """
    Then the response status should be "Bad Request"
    And the response should be
    """
    {
    "data": null,
    "debug": "Unable to complete the requested operation with the given input values.",
    "message": "Data source DOESNOTEXIST not found",
    "status": 400,
    "type": "BadRequestException"
    }
    """


  Scenario: Search all data sources for document of type ValuesBlueprint
    Given i access the resource url "/api/v1/search"
    When i make a "POST" request
    """
    {
      "type": "blueprints/root_package/ValuesBlueprint"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "entities/1":     {
      "_id": "1",
      "name": "primitive_1",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 120.0,
      "an_integer": 5,
      "a_string": "abc"
    },
    "entities/2":     {
      "_id": "2",
      "name": "primitive_2",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 150.1,
      "an_integer": 10,
      "a_string": "def"
    },
    "moreEntities/99": {
      "_id": "99",
      "name": "primitive_more",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 10.0,
      "an_integer": 10,
      "a_string": "def"
      }
    }
    """