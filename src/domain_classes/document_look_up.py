from pydantic import BaseModel

from authentication.access_control import ACL


class DocumentLookUp(BaseModel):
    lookup_id: str
    repository: str
    database_id: str
    acl: ACL
