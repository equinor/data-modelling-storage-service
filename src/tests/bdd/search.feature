# Created by kristian at 02.08.2021
Feature: seach

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
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "2",
                "name": "PackageA",
                "type": "system/SIMOS/Package"
            },
            {
                "_id": "3",
                "name": "PackageB",
                "type": "system/SIMOS/Package"
            }
        ]
    }
    """

    Given there exist document with id "2" in data source "data-source-name"
    """
    {
      "name": "PackageA",
      "description": "",
      "type": "system/SIMOS/Package",
      "isRoot": false,
      "content": [
          {
              "_id": "4",
              "name": "Parent",
              "type": "system/SIMOS/Blueprint"
          }
      ]
    }
    """

    Given there exist document with id "3" in data source "data-source-name"
    """
    {
      "name": "PackageB",
      "description": "",
      "type": "system/SIMOS/Package",
      "isRoot": false,
      "content": [
            {
                "_id": "5",
                "name": "parentEntity",
                "type": "data-source-name/PackageA/Parent"
            }
      ]
    }
    """

    Given there exist document with id "4" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Parent",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "level",
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {}
    }
    """


    Scenario: find parent package
      Given I access the resource url "/api/v1/findPackages/data-source-name/5"
      When I make a "GET" request
      Then the response status should be "OK"
      And the response should contain
      """
        [{"package_id": "1", "package_name": "root_package", "is_root": true, "child_id": "3"}, {"package_id": "3", "package_name": "PackageB", "is_root": false, "child_id": "5"}]
      """