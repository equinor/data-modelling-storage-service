Feature: Exporting root packages
    Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

    Given there are documents for the data source "test-DS" in collection "test-DS"
      | uid | parent_uid | name          | type                   |
      | 4fd85b95-0c60-4e28-87fa-e767b26b41c5   |            | blueprints    | dmss://system/SIMOS/Package   |
      | 5ad85b95-0c60-4e28-87fa-e767b26b41c5   | 4fd85b95-0c60-4e28-87fa-e767b26b41c5          | sub_package_1 | dmss://system/SIMOS/Package   |
      | 6bd85b95-0c60-4e28-87fa-e767b26b41c5   | 5ad85b95-0c60-4e28-87fa-e767b26b41c5          | document_1    | dmss://system/SIMOS/Blueprint |


  Scenario: A user want's to export a root package
    Given I access the resource url "/api/export/test-DS/blueprints"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"

