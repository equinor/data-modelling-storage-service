Feature: Exporting root packages
    Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |


    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestDataPackage",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [
        {
          "address": "$2",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$3",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "SomeBlueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
        "name": "somePackage",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": false,
        "content": [
                  {
          "address": "$4",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
        ]
    }
    """
    Given there exist document with id "4" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "AnotherBlueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """


  Scenario: A user wants to export a root package using path
    Given I access the resource url "/api/export/test-DS/TestDataPackage"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"
    Given I access the resource url "/api/export/dmss://test-DS/TestDataPackage"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"

  Scenario: A user wants to export a package using path
    Given I access the resource url "/api/export/test-DS/TestDataPackage/somePackage"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"
    Given I access the resource url "/api/export/dmss://test-DS/TestDataPackage/somePackage"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"


  Scenario: A user wants to export a single document using path
    Given I access the resource url "/api/export/test-DS/TestDataPackage/SomeBlueprint"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"
    Given I access the resource url "/api/export/dmss://test-DS/TestDataPackage/SomeBlueprint"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"


