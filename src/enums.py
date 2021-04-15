from enum import auto, Enum

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


class DataSourceType(Enum):
    MONGO = "mongo-db"
    AZURE_BLOB_STORAGE = "azure-blob-storage"
    LOCAL = "localStorage"

    @staticmethod
    def has_value(value):
        values = [item.value for item in DataSourceType]
        return value in values


class RepositoryType(Enum):
    DocumentRepository = auto()
    PackageRepository = auto()
    BlueprintRepository = auto()


class StorageDataTypes(Enum):
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
    DATA_SOURCE_TYPE = "data-source"


class DMT(Enum):
    PACKAGE = "system/SIMOS/Package"
    ENTITY = "system/SIMOS/Entity"
