Feature: Get document

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      |       name         |
      | test-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database    | collection | type     | dataTypes    |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo  | bdd-test    | blob-data  | mongo-db | default,blob |


    Given there exist document with id "1" in data source "test-source-name"
    """
    {
        "name": "TestData",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "content": [
            {
                "address": "$55",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$66",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$77",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }

        ],
        "isRoot": true
    }
    """
    
  Given there exist document with id "55" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "BlueprintWithOptionalAttributes",
      "attributes": [
        {
          "name": "type",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "name",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "AnExtraValue",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "Hobby",
          "attributeType": "dmss://test-source-name/TestData/Hobby",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": "true"
        }
      ]
    }
    """

    Given there exist document with id "66" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Hobby",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "difficulty",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

    Given there exist document with id "77" in data source "test-source-name"
    """
    {
      "type": "dmss://test-source-name/TestData/BlueprintWithOptionalAttributes",
      "name": "example",
      "AnExtraValue": "something"
    }
    """



  Scenario: when fetching entity by id, optional attributes should not be included
    Given I access the resource url "/api/documents/test-source-name/$77?depth=1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "_id": "77",
      "type": "dmss://test-source-name/TestData/BlueprintWithOptionalAttributes",
      "name": "example",
      "AnExtraValue": "something"
    }
    """

  Scenario: when fetching entity by path, optional attributes should not be included
    Given I access the resource url "/api/documents/test-source-name/TestData/example/?depth=1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "_id": "77",
      "type": "dmss://test-source-name/TestData/BlueprintWithOptionalAttributes",
      "name": "example",
      "AnExtraValue": "something"
    }
    """