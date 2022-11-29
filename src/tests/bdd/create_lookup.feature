Feature: Create a lookup table

  Scenario: Create a lookup table
    Given i access the resource url "/api/v1/lookup/my-new-lookup"
    When i make a "POST" request
    """
    {
      "uiRecipes": {
        "someDS/aPackage/myBlueprint": [
          {
            "type": "sys://system/SIMOS/UiRecipe",
            "name": "MySignalView",
            "plugin": "signal-plot"
          }
        ]
      }
    }
    """
    Then the response status should be "No Content"
