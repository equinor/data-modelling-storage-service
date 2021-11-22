from pydantic import constr, Field, root_validator, UUID4
from pydantic.main import BaseModel, Extra
from typing import Optional

# Only allow characters a-9 and '_' + '-'
name_regex = "^[A-Za-z0-9_-]*$"


class EntityName(BaseModel):
    name: constr(min_length=1, max_length=128, regex=name_regex, strip_whitespace=True)


class OptionalEntityName(BaseModel):
    name: Optional[constr(min_length=1, max_length=128, regex=name_regex, strip_whitespace=True)]


class EntityType(BaseModel):
    # Regex only allow characters a-9 and '_' + '-' + '/' for paths
    type: constr(min_length=3, max_length=128, regex=r"^[A-Za-z0-9_\/-]*$", strip_whitespace=True)  # noqa


class DataSource(BaseModel):
    data_source_id: constr(min_length=3, max_length=128, regex=name_regex, strip_whitespace=True)


class EntityUUID(BaseModel):
    uid: UUID4 = Field(..., alias="_id")


class Reference(EntityType, EntityName, EntityUUID):
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}


class UncontainedEntity(EntityType, OptionalEntityName, EntityUUID, extra=Extra.allow):
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}

    def to_dict(self):
        if self.name is not None:
            return self.dict()
        else:
            return self.dict(exclude={"name"})


class BlueprintEntity(EntityType, EntityName, EntityUUID, extra=Extra.allow):
    # an entity that have type: system/SIMOS/Blueprint
    @root_validator(pre=True)
    def from_underscore_id_to_uid(cls, values):
        return {**values, "uid": values.get("_id")}


# An entity must have a type, but having a name is optional
class Entity(EntityType, OptionalEntityName, extra=Extra.allow):
    def to_dict(self):
        if self.name is not None:
            return self.dict()
        else:
            return self.dict(exclude={"name"})
