Feature: Export an entity's meta data

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

  Scenario: Fetch the meta of an entity with some meta info in root_package and some in the entity itself
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "_meta_": {
        "type": "CORE:Meta",
        "version": "0.0.1",
        "dependencies": [
          {
            "type": "dmss://system/SIMOS/Dependency",
            "alias": "CORE",
            "address": "system/SIMOS",
            "version": "0.0.1",
            "protocol": "dmss"
          }
        ]
      },
      "content": [
        {
          "address": "3f9ff99f-9cb5-4afc-947b-a3224eee341f",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """

    Given there exist document with id "3f9ff99f-9cb5-4afc-947b-a3224eee341f" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "some-entity",
      "_meta_": {
        "type": "CORE:Meta",
        "version": "0.0.1",
        "dependencies": [
          {
            "type": "dmss://system/SIMOS/Dependency",
            "alias": "TEST-MODELS",
            "address": "DemoApplicationDataSource/models",
            "version": "0.0.1",
            "protocol": "dmss"
          }
        ]
      },
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """
    Given i access the resource url "/api/export/meta/test-DS/TestData/some-entity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "CORE:Meta",
      "version": "0.0.1",
      "dependencies": [
        {
          "type": "dmss://system/SIMOS/Dependency",
          "alias": "CORE",
          "address": "system/SIMOS",
          "version": "0.0.1",
          "protocol": "dmss"
        },
        {
          "type": "dmss://system/SIMOS/Dependency",
          "alias": "TEST-MODELS",
          "address": "DemoApplicationDataSource/models",
          "version": "0.0.1",
          "protocol": "dmss"
        }
      ]
    }
    """

  Scenario: Fetch the meta of an entity with no meta data defined
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [
        {
          "address": "3f9ff99f-9cb5-4afc-947b-a3224eee341f",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """

    Given there exist document with id "3f9ff99f-9cb5-4afc-947b-a3224eee341f" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "some-entity",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """
    Given i access the resource url "/api/export/meta/test-DS/TestData/some-entity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {}
    """

  Scenario: Fetch the meta of a root package
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "_meta_": {
        "type": "CORE:Meta",
        "version": "0.0.1",
        "dependencies": [
          {
            "type": "dmss://system/SIMOS/Dependency",
            "alias": "CORE",
            "address": "system/SIMOS",
            "version": "0.0.1",
            "protocol": "dmss"
          }
        ]
      },
      "content": [
        {
          "address": "3f9ff99f-9cb5-4afc-947b-a3224eee341f",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """
    Given i access the resource url "/api/export/meta/test-DS/TestData/"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "CORE:Meta",
      "version": "0.0.1",
      "dependencies": [
        {
          "type": "dmss://system/SIMOS/Dependency",
          "alias": "CORE",
          "address": "system/SIMOS",
          "version": "0.0.1",
          "protocol": "dmss"
        }
      ]
    }
    """