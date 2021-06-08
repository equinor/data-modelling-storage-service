from typing import Callable, List


def valid_extended_type(type: str, extended_types: List[str], get_blueprint: Callable) -> bool:
    if type in extended_types:
        return True
    for inherited_type in extended_types:
        blueprint = get_blueprint(inherited_type)
        if type in blueprint.extends:
            return True
        if valid_extended_type(type, blueprint.extends, get_blueprint):
            return True
