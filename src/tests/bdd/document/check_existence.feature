# Created by christopher.lokken at 24/08/2023
Feature: Check the existence of documents

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

  Scenario: Check the existence of non-existing document
    Given I access the resource url "/api/documents-existence/test-DS/$1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    true
    """
    Given I access the resource url "/api/documents-existence/test-DS/$2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    false
    """