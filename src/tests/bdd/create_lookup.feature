Feature: Create a lookup table

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      | name    |
      | test-DS |


    Given there exist document with id "100" in data source "test-DS"
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
                      "address": "$103",
                      "type": "dmss://system/SIMOS/Reference",
                      "referenceType": "link"
                  }
              ]
          }
          """

    Given there exist document with id "101" in data source "test-DS"
      """
      {
          "name": "recipe_links",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": false,
          "content": [
              {
                  "address": "$102",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              }
          ]
      }
      """

    Given there exist document with id "102" in data source "test-DS"
      """
      {
        "type": "dmss://system/SIMOS/RecipeLink",
        "_blueprintPath_": "_default_",
        "uiRecipes": [
          {
            "name": "Edit",
            "type": "dmss://system/SIMOS/UiRecipe",
            "plugin": "@development-framework/dm-core-plugins/form",
            "category": "edit"
          }
        ]
      }
      """

    Given there exist document with id "103" in data source "test-DS"
      """
      {
          "name": "more_recipe_links",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": false,
          "content": [
              {
                  "address": "$104",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              }
          ]
      }
      """

    Given there exist document with id "104" in data source "test-DS"
      """
      {
        "type": "dmss://system/SIMOS/RecipeLink",
        "_blueprintPath_": "dmss://system/SIMOS/NamedEntity",
        "uiRecipes": [
          {
            "name": "Yaml",
            "type": "dmss://system/SIMOS/UiRecipe",
            "plugin": "@development-framework/dm-core-plugins/yaml"
          }
        ]
      }
      """


  Scenario: System admins want to create a recipe lookup for the DMSS - SIMOS/recipe_links folder
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"

  Scenario: System admins want to replace an existing recipe lookup for DMSS - SIMOS/recipe_links folder
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"

  Scenario: System admins want to use several package paths to create a lookup table
    Given i access the resource url "/api/application/test-DS?recipe_package=test-DS/root_package/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "_default_": [
          {
            "name": "Edit",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/form",
            "category": "edit",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "_default_": []
      },
      "initial_ui_recipes": {
        "_default_": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/recipe_links"]
    }
    """
    Given i access the resource url "/api/application/test-DS?recipe_package=test-DS/root_package/recipe_links&recipe_package=test-DS/root_package/more_recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "_default_": [
          {
            "name": "Edit",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/form",
            "category": "edit",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ],
        "dmss://system/SIMOS/NamedEntity": [
          {
            "name": "Yaml",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/yaml",
            "category": "",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "_default_": [],
        "dmss://system/SIMOS/NamedEntity": []
      },
      "initial_ui_recipes": {
        "_default_": null,
        "dmss://system/SIMOS/NamedEntity": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/recipe_links", "test-DS/root_package/more_recipe_links"]
    }
    """

  Scenario: System admins want to replace an existing recipe lookup (test-DS/root_package/recipe_links) with a new one (test-DS/root_package/more_recipe_links)
    Given i access the resource url "/api/application/test-DS?recipe_package=test-DS/root_package/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "_default_": [
          {
            "name": "Edit",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/form",
            "category": "edit",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "_default_": []
      },
      "initial_ui_recipes": {
        "_default_": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/recipe_links"]
    }
    """
    Given i access the resource url "/api/application/test-DS?recipe_package=test-DS/root_package/more_recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "dmss://system/SIMOS/NamedEntity": [
          {
            "name": "Yaml",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/yaml",
            "category": "",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "dmss://system/SIMOS/NamedEntity": []
      },
      "initial_ui_recipes": {
        "dmss://system/SIMOS/NamedEntity": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/more_recipe_links"]
    }
    """

  Scenario: System admins want to recreate an existing recipe lookup after updating the default ui_recipe
    Given i access the resource url "/api/application/test-DS?recipe_package=test-DS/root_package/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "_default_": [
          {
            "name": "Edit",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "@development-framework/dm-core-plugins/form",
            "category": "edit",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "_default_": []
      },
      "initial_ui_recipes": {
        "_default_": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/recipe_links"]
    }
    """
    Given i access the resource url "/api/documents/test-DS/$102"
    When i make a form-data "PUT" request
      """
      {"data":       {
        "type": "dmss://system/SIMOS/RecipeLink",
        "_blueprintPath_": "_default_",
        "uiRecipes": [
          {
            "name": "THIS CHANGED",
            "type": "dmss://system/SIMOS/UiRecipe",
            "plugin": "SOME OTHER PLUGIN",
            "category": "edit"
          }
        ]
      }}
      """
    Then the response status should be "OK"
    Given i access the resource url "/api/application/test-DS/refresh"
    When i make a "POST" request
    Then the response status should be "OK"
    Given i access the resource url "/api/application/test-DS"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "ui_recipes": {
        "_default_": [
          {
            "name": "THIS CHANGED",
            "type": "dmss://system/SIMOS/UiRecipe",
            "attributes": [],
            "description": "",
            "plugin": "SOME OTHER PLUGIN",
            "category": "edit",
            "roles": null,
            "config": null,
            "label": "",
            "dimensions": "",
            "showRefreshButton": false
          }
        ]
      },
      "storage_recipes": {
        "_default_": []
      },
      "initial_ui_recipes": {
        "_default_": null
      },
      "extends": {},
      "paths": ["test-DS/root_package/recipe_links"]
    }
    """

