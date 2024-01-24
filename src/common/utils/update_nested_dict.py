def update_nested_dict(nested_dict: dict, path_to_update: list[str], new_value: dict):
    if len(path_to_update) == 1:
        key = path_to_update[0]
        if isinstance(nested_dict, dict):
            nested_dict[key] = new_value
        else:
            nested_dict[int(key)] = new_value
    else:
        key = path_to_update[0]
        if isinstance(nested_dict, dict) and key in nested_dict:
            update_nested_dict(nested_dict[key], path_to_update[1:], new_value)
        else:
            update_nested_dict(nested_dict[int(key)], path_to_update[1:], new_value)
