def to_dot_notation(path):
    dot_path = []
    for index, path_entry in enumerate(path):
        if index == 0:
            dot_path.append(str(path_entry))
        # Next is not a list
        elif str(path_entry)[0] != "[":
            dot_path.append("." + str(path_entry))
        else:
            dot_path.append(str(path_entry))
    return "".join([str(dot_path_entry) for dot_path_entry in dot_path])
