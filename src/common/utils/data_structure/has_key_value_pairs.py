def has_key_value_pairs(target: dict, content: dict):
    """Util method for checking that target entity contains the key-value pairs defined in content"""
    return all(key in target and target[key] == value for key, value in content.items())
