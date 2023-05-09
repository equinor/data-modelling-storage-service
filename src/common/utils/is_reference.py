from enums import REFERENCE_TYPES, SIMOS


def is_reference(entity):
    return isinstance(entity, dict) and (entity.get("type") == SIMOS.REFERENCE.value)


def is_link(reference: dict) -> bool:
    return reference.get("referenceType", REFERENCE_TYPES.LINK.value) == REFERENCE_TYPES.LINK.LINK
