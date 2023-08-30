Feature: Add document with optional attributes

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      |       name         |
      | data-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database  | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      |  bdd-test | documents  | mongo-db | default      |

    Given there exist document with id "100" in data source "data-source-name"
      """
      {
          "name": "root_package",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": true,
          "content": [
              {
                  "address": "$101",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$102",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$103",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$workComputerId",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              }
          ]
      }
      """

    Given there exist document with id "103" in data source "data-source-name"
    """
    {
      "name": "KeyboardKey",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": [
        "dmss://system/SIMOS/NamedEntity"
      ],
      "description": "",
      "attributes": []
      }
    """

    Given there exist document with id "101" in data source "data-source-name"
      """
      {
      "name": "Computer",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": [
        "dmss://system/SIMOS/NamedEntity"
      ],
      "description": "",
      "attributes": [
          {
            "name": "model",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
          },
          {
            "name": "keyboard",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "data-source-name/root_package/Keyboard",
            "optional": true
          },
          {
            "name": "letterKeys",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "data-source-name/root_package/KeyboardKey",
            "optional": true,
            "dimensions": "*"
          },
          {
            "name": "numberKeys",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "data-source-name/root_package/KeyboardKey",
            "optional": true,
            "dimensions": "*"
          }
        ]
      }
     """

    Given there exist document with id "102" in data source "data-source-name"
      """
      {
        "name": "Keyboard",
        "type": "dmss://system/SIMOS/Blueprint",
        "extends": [
          "dmss://system/SIMOS/NamedEntity"
        ],
        "attributes": [
          {
            "name": "language",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
          }
        ]
      }
      """

    Given there exist document with id "workComputerId" in data source "data-source-name"
      """
      {
        "type": "data-source-name/root_package/Computer",
        "name": "workComputer",
        "model": "Dell",
        "letterKeys": []
      }
      """


  Scenario: add optional attribute that does not exist
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.keyboard"
    When I make a "POST" request with "1" files
    """
    {
      "document":
       {
        "name": "dellKeyboard",
        "type": "data-source-name/root_package/Keyboard",
        "language": "EN"
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "uid": "workComputerId.keyboard"
      }
    """
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.keyboard"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "name": "dellKeyboard",
      "type": "data-source-name/root_package/Keyboard",
      "language": "EN"
    }
    """

  Scenario: add to list that exist
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.letterKeys"
    When I make a "POST" request with "1" files
    """
    {
      "document":
       {
        "name": "T",
        "type": "data-source-name/root_package/KeyboardKey"
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "uid": "workComputerId.letterKeys.0"
      }
    """
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.letterKeys"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    [
     {
       "name": "T",
       "type": "data-source-name/root_package/KeyboardKey"
     }
    ]
    """


  Scenario: add to list that does not exist
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.numberKeys"
    When I make a "POST" request with "1" files
    """
    {
      "document":
      {
        "name": "7",
        "type": "data-source-name/root_package/KeyboardKey"
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "uid": "workComputerId.numberKeys"
      }
    """
    Given i access the resource url "/api/documents/data-source-name/$workComputerId.numberKeys[0]"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
     {
       "name": "7",
       "type": "data-source-name/root_package/KeyboardKey"
     }
    """

  Scenario: add to a package that does not exist should fail
    Given i access the resource url "/api/documents/data-source-name/non-existing-package"
    When I make a "POST" request with "1" files
    """
    {
      "document":
       {
        "name": "@",
        "type": "data-source-name/root_package/KeyboardKey"
      }
    }
    """
    Then the response status should be "Not Found"

