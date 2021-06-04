from enum import Enum

PRIMITIVES = {"string", "number", "integer", "boolean"}
BLOB_TYPES = ("system/SIMOS/blob_types/PDF",)

REQUIRED_ATTRIBUTES = ("name", "type")


class PrimitiveDataTypes(Enum):
    STR = "string"
    NUM = "number"
    INT = "integer"
    BOOL = "boolean"

    def to_py_type(self):
        if self is PrimitiveDataTypes.BOOL:
            return bool
        elif self is PrimitiveDataTypes.INT:
            return int
        elif self is PrimitiveDataTypes.NUM:
            return float
        elif self is PrimitiveDataTypes.STR:
            return str


class RepositoryType(Enum):
    MONGO = "mongo-db"
    AZURE_BLOB_STORAGE = "azure-blob-storage"
    LOCAL = "localStorage"

    @staticmethod
    def has_value(value):
        if next((item for item in RepositoryType if item.value == value), None):
            return True


class StorageDataTypes(str, Enum):
    DEFAULT = "default"
    LARGE = "large"
    VERY_LARGE = "veryLarge"
    VIDEO = "video"
    BLOB = "blob"


class SIMOS(Enum):
    BLUEPRINT = "system/SIMOS/Blueprint"
    BLUEPRINT_ATTRIBUTE = "system/SIMOS/BlueprintAttribute"
    APPLICATION = "system/SIMOS/Application"
    ATTRIBUTE_TYPES = "system/SIMOS/AttributeTypes"


class DMT(Enum):
    PACKAGE = "system/SIMOS/Package"
    ENTITY = "system/SIMOS/Entity"
    DATASOURCE = "datasource"
