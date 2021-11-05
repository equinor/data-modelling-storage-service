from jose import jwt

from domain_classes.user import User
from config import default_user

rsa_private_key = """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""


def generate_token(user: User = default_user):
    """
    This function is for testing purposes only
    Used for behave testing
    """
    # https://docs.microsoft.com/en-us/azure/active-directory/develop/id-tokens#claims-in-an-id-token
    payload = {
        "name": user.full_name,
        "preferred_username": user.email,
        "scp": "FoR_test_scope",
        "sub": user.username,
        "roles": user.roles,
    }
    token = jwt.encode(payload, rsa_private_key, algorithm="RS256")
    return token
