from utils.token_generator import generate_token as token_generator
from domain_classes.user import User

test_user = User(**{"username": "behave-test", "full_name": "Behave Test", "email": "behave-test@example.com"})


def generate_token(user: User = test_user):
    return token_generator(user)
