Feature: Relative references

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |
      | test-source-name |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     | bdd-test | documents  | mongo-db | default      |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo | bdd-test | blob-data  | mongo-db | default,blob |
      | data-source-name | db   | 27017 | maf      | maf      | false | doc-repo  | bdd-test | test       | mongo-db | default      |

    Given there exist document with id "2" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Task",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "dmss://test-source-name/TestData/Data",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "data"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/Job",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "job",
          "optional": true
        }
      ]
    }
    """

    Given there exist document with id "4" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Data",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "aNumber",
          "type": "CORE:BlueprintAttribute",
          "attributeType": "number"
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Job",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "input",
          "type": "CORE:BlueprintAttribute",
          "description": "Input",
          "attributeType": "object",
          "label": "Input",
          "contained": false,
          "optional": true
        }
      ]
    }
    """

    Given there exist document with id "1" in data source "test-source-name"
    """
    {
        "name": "TestData",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "content": [
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$2",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$4",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$5",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }

        ],
        "isRoot": true
    }
    """

    Given there exist document with id "5" in data source "test-source-name"
    """
    {
      "type": "dmss://test-source-name/TestData/Task",
      "name": "TestData",
      "data": {
        "type": "dmss://test-source-name/TestData/Data",
        "aNumber": 100
      },
      "job": {
        "type": "dmss://test-source-name/TestData/Job",
        "name": "Job",
        "input": {
          "address": "~.~.data",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      }
    }
    """

  Scenario: Get document that contains a relative references
    Given I access the resource url "/api/documents/test-source-name/$5"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "dmss://test-source-name/TestData/Task",
      "name": "TestData",
      "data": {
        "type": "dmss://test-source-name/TestData/Data",
        "aNumber": 100
      },
      "job": {
        "type": "dmss://test-source-name/TestData/Job",
        "name": "Job",
        "input": {
          "address": "~.~.data",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      }
    }
    """

  Scenario: Resolve relative references
    Given I access the resource url "/api/documents/test-source-name/$5.job.input?depth=1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "dmss://test-source-name/TestData/Data",
      "aNumber": 100
    }
    """