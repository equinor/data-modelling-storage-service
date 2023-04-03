from enums import SIMOS


def is_reference(entity):
    return isinstance(entity, dict) and (
        entity.get("type") == SIMOS.STORAGE_ADDRESS.value or entity.get("type") == SIMOS.LINK.value
    )
