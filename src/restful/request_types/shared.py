from typing import Annotated

from pydantic import UUID4, Field, StringConstraints
from pydantic.main import BaseModel, ConfigDict

# Only allow characters a-9 and '_' + '-'
NameConstrainedString = Annotated[
    str, StringConstraints(min_length=1, max_length=128, pattern="^[A-Za-z0-9_-]*$", strip_whitespace=True)
]

# Regex only allow characters a-9 and '_' + '-' + '/' + ':' for paths
TypeConstrainedString = Annotated[
    str, StringConstraints(min_length=3, max_length=128, pattern=r"^[A-Z:a-z0-9_\/-]*$", strip_whitespace=True)
]


def pop_additional_props(s):
    s.pop("additionalProperties")


class Entity(BaseModel):
    type: TypeConstrainedString
    # Our openapi python generator (v7.3.0) does not support OpenApi v3.1, and fails unless we remove
    # the field "additionalProperties"
    model_config = ConfigDict(extra="allow", json_schema_extra=pop_additional_props)


class EntityName(BaseModel):
    name: NameConstrainedString


class OptionalEntityName(BaseModel):
    name: NameConstrainedString | None


class DataSource(BaseModel):
    data_source_id: NameConstrainedString


class DataSourceList(BaseModel):
    data_sources: list[NameConstrainedString]


class EntityUUID(BaseModel):
    uid: UUID4 = Field(..., alias="_id")


class ReferenceEntity(BaseModel):
    address: str
    type: TypeConstrainedString
    referenceType: str


class UncontainedEntity(Entity, OptionalEntityName, EntityUUID):
    model_config = ConfigDict(extra="allow")

    def to_dict(self):
        if self.name is not None:
            return self.dict(by_alias=True)

        return self.dict(exclude={"name"})
