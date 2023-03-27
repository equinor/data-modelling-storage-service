from typing import Optional

from pydantic import UUID4, Field, constr, root_validator
from pydantic.main import BaseModel, Extra

# Only allow characters a-9 and '_' + '-'
common_name_constrained_string = constr(min_length=1, max_length=128, regex="^[A-Za-z0-9_-]*$", strip_whitespace=True)

# Regex only allow characters a-9 and '_' + '-' + '/' for paths
common_type_constrained_string = constr(
    min_length=3, max_length=128, regex=r"^[A-Z:a-z0-9_\/-]*$", strip_whitespace=True
)  # noqa


class EntityName(BaseModel):
    name: common_name_constrained_string  # type: ignore


class OptionalEntityName(BaseModel):
    name: Optional[common_name_constrained_string]  # type: ignore


class EntityType(BaseModel):
    type: common_type_constrained_string  # type: ignore


class DataSource(BaseModel):
    data_source_id: common_name_constrained_string  # type: ignore


class DataSourceList(BaseModel):
    data_sources: list[common_name_constrained_string]  # type: ignore


class EntityUUID(BaseModel):
    uid: UUID4 = Field(..., alias="_id")


class Reference(BaseModel):
    # TODO: uid can also be dotted path
    uid: str = Field(..., alias="ref")
    type: common_type_constrained_string  # type: ignore
    targetType: Optional[common_type_constrained_string]  # type: ignore
    targetName: Optional[common_name_constrained_string]  # type: ignore

    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("ref")}


class UncontainedEntity(EntityType, OptionalEntityName, EntityUUID, extra=Extra.allow):  # type: ignore
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}

    def to_dict(self):
        if self.name is not None:
            return self.dict(by_alias=True)

        return self.dict(exclude={"name"})


class BlueprintEntity(EntityType, EntityName, EntityUUID, extra=Extra.allow):  # type: ignore
    # an entity that have type: system/SIMOS/Blueprint
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}


# An entity must have a type, but having a name is optional
class Entity(EntityType, OptionalEntityName, extra=Extra.allow):  # type: ignore
    def to_dict(self):
        if self.name is not None:
            return self.dict(by_alias=True)
        else:
            return self.dict(exclude={"name"})
