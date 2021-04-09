from pydantic import constr, UUID4
from pydantic.main import BaseModel, Extra

# Only allow characters a-9 and '_' + '-'
name_regex = "^[A-Za-z0-9_-]*$"


class EntityName(BaseModel):
    name: constr(min_length=1, max_length=128, regex=name_regex, strip_whitespace=True)


class EntityType(BaseModel):
    # Regex only allow characters a-9 and '_' + '-' + '/' for paths
    type: constr(min_length=3, max_length=128, regex="^[A-Za-z0-9_\/-]*$", strip_whitespace=True)  # noqa


class DataSource(BaseModel):
    data_source_id: constr(min_length=3, max_length=128, regex=name_regex, strip_whitespace=True)


class UUIDType(BaseModel):
    uid: UUID4


class NamedEntity(EntityType, EntityName, extra=Extra.allow):
    pass
