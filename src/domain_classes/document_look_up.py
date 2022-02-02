from pydantic import BaseModel

from authentication.models import ACL


class DocumentLookUp(BaseModel):
    lookup_id: str
    repository: str
    database_id: str
    acl: ACL
