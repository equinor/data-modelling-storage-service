Feature: Blueprint - Resolve path to document use case

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |


    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | documents      | mongo-db | default   |

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                     |
      | 1   |            | blueprints    |             | dmss://system/SIMOS/Package     |
      | 2   | 1          | sub_package_1 |             | dmss://system/SIMOS/Package     |
      | 3   | 2          | document_1    |             | dmss://system/SIMOS/Blueprint   |


    Scenario: resolve path to document in the blueprints package
      Given I access the resource url "/api/resolve-path/data-source-name/3"
      When I make a "GET" request
      Then the response status should be "OK"
      And the response should be
      """
      dmss://data-source-name/blueprints/sub_package_1/document_1
      """

    Scenario: resolve path to document fails when document with id does not exist
      Given I access the resource url "/api/resolve-path/data-source-name/99"
      When I make a "GET" request
      Then the response status should be "Not Found"


