from pydantic.main import BaseModel

from authentication.models import User
from restful.use_case import UseCase


class MoveRequest(BaseModel):
    source: str
    destination: str


class MoveFileUseCase(UseCase):
    def __init__(self, user: User, get_repository):
        self.user = user
        self.get_repository = get_repository

    def process_request(self, req: MoveRequest):
        raise NotImplementedError
