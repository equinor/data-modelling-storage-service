def has_key_value_pairs(target: dict, content: dict):
    """Util method for checking that target entity contains the key-value pairs defined in content"""
    is_identical = True
    for key in content:
        if key not in target:
            raise KeyError(f"They key '{key}' does not exist in target {str(target)}")
        if target[key] != content[key]:
            is_identical = False
    return is_identical
