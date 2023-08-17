from typing import Optional

from pydantic import UUID4, Field, constr, root_validator
from pydantic.main import BaseModel, Extra

# Only allow characters a-9 and '_' + '-'
NameConstrainedString = constr(min_length=1, max_length=128, regex="^[A-Za-z0-9_-]*$", strip_whitespace=True)

# Regex only allow characters a-9 and '_' + '-' + '/' for paths
TypeConstrainedString = constr(
    min_length=3, max_length=128, regex=r"^[A-Z:a-z0-9_\/-]*$", strip_whitespace=True
)  # noqa


class Entity(BaseModel, extra=Extra.allow):
    type: TypeConstrainedString  # type: ignore


class EntityName(BaseModel):
    name: NameConstrainedString  # type: ignore


class OptionalEntityName(BaseModel):
    name: Optional[NameConstrainedString]  # type: ignore


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


class UncontainedEntity(Entity, OptionalEntityName, EntityUUID, extra=Extra.allow):  # type: ignore
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}

    def to_dict(self):
        if self.name is not None:
            return self.dict(by_alias=True)

        return self.dict(exclude={"name"})


class BlueprintEntity(Entity, EntityName, EntityUUID, extra=Extra.allow):  # type: ignore
    # an entity that have type: system/SIMOS/Blueprint
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}
