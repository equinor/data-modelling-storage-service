from typing import Optional

from authentication.models import PATData, User
from services.database import personal_access_token_collection
from utils.encryption import scrypt


def insert_pat(pat: PATData) -> None:
    personal_access_token_collection.insert_one(pat.dict())


def get_pat(pat: str) -> Optional[PATData]:
    pat_id = scrypt(pat)  # Hash the token and lookup the PAT Object stored with that hash as an '_id'
    pat_dict = personal_access_token_collection.find_one(filter={"_id": pat_id})
    if not pat_dict:
        return None
    return PATData(**pat_dict)


def get_users_pats(user: User) -> list[PATData]:
    # Filter out the hashed "_id" attribute
    pat_list = [
        pat
        for pat in personal_access_token_collection.find(
            filter={"username_id": user.username_id}, projection={"_id": False}
        )
    ]
    return pat_list


def delete_pat(pat_id: str, user: User) -> None:
    personal_access_token_collection.delete_one(filter={"uuid": pat_id, "username_id": user.username_id}).acknowledged
