import hashlib


def generate_hash(path: str, length: int = 8) -> str:
    # Generate a SHA-256 hash and truncate it to the desired length
    full_hash = hashlib.sha256(path.encode()).hexdigest()
    return "_" + full_hash[:length]
