from pydantic import BaseModel

from authentication.models import AccessControlList


class DocumentLookUp(BaseModel):
    lookup_id: str
    repository: str
    database_id: str
    acl: AccessControlList
    storage_affinity: str
    meta: dict | None = None
