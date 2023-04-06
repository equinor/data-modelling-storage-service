Feature: Get correct data for subtypes

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | documents  | mongo-db | default   |
      | data-source-name | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | test       | mongo-db | blob      |


    Given there exist document with id "1" in data source "data-source-name"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "ref": "3",
                "targetName": "BaseChild",
                "targetType": "dmss://system/SIMOS/Blueprint",
                "type": "dmss://system/SIMOS/Link"
            },
            {
                "ref": "4",
                "targetName": "Parent",
                "targetType": "dmss://system/SIMOS/Blueprint",
                "type": "dmss://system/SIMOS/Link"
            },
            {
                "ref": "5",
                "targetName": "SpecialChild",
                "targetType": "dmss://system/SIMOS/Blueprint",
                "type": "dmss://system/SIMOS/Link"
            },
            {
                "ref": "7",
                "targetName": "parentEntity",
                "targetType": "data-source-name/root_package/Parent",
                "type": "dmss://system/SIMOS/Link"
            }
        ]
    }
    """

    Given there exist document with id "3" in data source "data-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "BaseChild",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "AValue",
        "attributeType": "integer",
        "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """


    Given there exist document with id "4" in data source "data-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Parent",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "SomeChild",
        "attributeType": "data-source-name/root_package/BaseChild",
        "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "data-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "SpecialChild",
      "description": "",
      "extends": ["data-source-name/root_package/BaseChild"],
      "attributes": [
        {
          "name": "AnExtraValue",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """




  Given there exist document with id "7" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {
        "name": "specialChildInParent2",
        "type": "data-source-name/root_package/SpecialChild",
        "description": "special child type",
        "AValue": 222,
        "AnExtraValue": "extra value"
      }
    }
    """

  Given there exist document with id "8" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity2",
      "description": "",
      "SomeChild": {
        "name": "baseChildInParent",
        "type": "data-source-name/root_package/BaseChild",
        "description": "base child type",
        "AValue": 333
      }
    }
    """

  Scenario: fetch entity with a subtype attribute
    Given i access the resource url "/api/documents/data-source-name/7"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "_id": "7",
       "name": "parentEntity",
       "type": "data-source-name/root_package/Parent",
       "description": "",
       "SomeChild":
        {
          "name": "specialChildInParent2",
          "type": "data-source-name/root_package/SpecialChild",
          "description": "special child type",
          "AValue": 222,
          "AnExtraValue": "extra value"
        }
    }
    """


  Scenario: fetch entity with original attribute type
    Given i access the resource url "/api/documents/data-source-name/8"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "_id": "8",
       "name": "parentEntity2",
       "type": "data-source-name/root_package/Parent",
       "description": "",
       "SomeChild":
        {
          "name": "baseChildInParent",
          "type": "data-source-name/root_package/BaseChild",
          "description": "base child type",
          "AValue": 333
        }
    }
    """

