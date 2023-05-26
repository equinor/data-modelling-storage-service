def get_address(data_source_id: str, reference: dict) -> str:
    """Utility method to get address of reference"""
    if "://" in reference["address"]:
        # Already contains a data source id
        return reference["address"]
    else:
        return f"{data_source_id}/{reference['address']}"
