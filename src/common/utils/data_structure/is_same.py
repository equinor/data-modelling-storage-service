def is_same(target: dict, content: dict):
    """Util method that for checking that target document contains the content."""
    is_identical = True
    for key in content:
        if key not in target:
            raise KeyError(f"They key '{key}' does not exist in target {str(target)}")
        if target[key] != content[key]:
            is_identical = False
    return is_identical
