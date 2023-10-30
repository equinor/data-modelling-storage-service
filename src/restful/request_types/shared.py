from typing import Annotated

from pydantic import UUID4, ConfigDict, Field, StringConstraints, model_validator
from pydantic.main import BaseModel

# Only allow characters a-9 and '_' + '-'
NameConstrainedString = Annotated[
    str, StringConstraints(min_length=1, max_length=128, pattern="^[A-Za-z0-9_-]*$", strip_whitespace=True)
]

# Regex only allow characters a-9 and '_' + '-' + '/' for paths
TypeConstrainedString = Annotated[
    str, StringConstraints(min_length=3, max_length=128, pattern=r"^[A-Z:a-z0-9_\/-]*$", strip_whitespace=True)
]


class Entity(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: TypeConstrainedString  # type: ignore


class EntityName(BaseModel):
    name: NameConstrainedString  # type: ignore


class OptionalEntityName(BaseModel):
    name: NameConstrainedString | None = None  # type: ignore


class DataSource(BaseModel):
    data_source_id: NameConstrainedString  # type: ignore


class DataSourceList(BaseModel):
    data_sources: list[NameConstrainedString]  # type: ignore


class EntityUUID(BaseModel):
    uid: UUID4 = Field(..., alias="_id")


class ReferenceEntity(BaseModel):
    address: str
    type: TypeConstrainedString  # type: ignore
    referenceType: str


class UncontainedEntity(Entity, OptionalEntityName, EntityUUID):  # type: ignore
    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    @classmethod
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}

    def to_dict(self):
        if self.name is not None:
            return self.dict(by_alias=True)

        return self.dict(exclude={"name"})


class BlueprintEntity(Entity, EntityName, EntityUUID):
    model_config = ConfigDict(extra="allow")

    # an entity that have type: system/SIMOS/Blueprint
    @model_validator(mode="before")
    @classmethod
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}
