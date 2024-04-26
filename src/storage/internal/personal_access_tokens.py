from authentication.models import PATData, User
from common.utils.encryption import scrypt
from services.database import personal_access_token_db


def insert_pat(pat: PATData) -> None:
    personal_access_token_db.set(pat.pat_hash, pat.dict())


def get_pat(pat: str) -> PATData | None:
    pat_id = scrypt(pat)  # Hash the token and lookup the PAT Object stored with that hash as an '_id'
    if pat_dict := personal_access_token_db.get(pat_id):
        return PATData(**pat_dict)
    return None


# TODO: Use redis json for these, so we can query nested values
def get_users_pats(user: User) -> list[dict]:
    users_pats = []
    for pat_key in personal_access_token_db.list_keys():
        if pat := personal_access_token_db.get(pat_key):
            pat = PATData(**pat)
            if pat.user_id == user.user_id:
                pat_dict = pat.dict()
                # Filter out the hashed pat value used as "_id"
                del pat_dict["_id"]
                users_pats.append(pat_dict)
    return users_pats


def delete_pat(pat_id: str, user: User) -> None:
    for pat_key in personal_access_token_db.list_keys():
        if pat := personal_access_token_db.get(pat_key):
            if pat["user_id"] == user.user_id and pat["uuid"] == pat_id:
                personal_access_token_db.delete(pat["_id"])
                return
