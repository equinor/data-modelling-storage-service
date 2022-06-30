from enum import Enum

PRIMITIVES = {"string", "number", "integer", "boolean"}


class BuiltinDataTypes(Enum):
    STR = "string"
    NUM = "number"
    INT = "integer"
    BOOL = "boolean"
    OBJECT = "object"  # Any complex type (i.e. any blueprint type)

    def to_py_type(self):
        if self is BuiltinDataTypes.BOOL:
            return bool
        elif self is BuiltinDataTypes.INT:
            return int
        elif self is BuiltinDataTypes.NUM:
            return float
        elif self is BuiltinDataTypes.STR:
            return str
        elif self is BuiltinDataTypes.OBJECT:
            return dict


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
    ENTITY = "system/SIMOS/Entity"
    PACKAGE = "system/SIMOS/Package"
    BLUEPRINT_ATTRIBUTE = "system/SIMOS/BlueprintAttribute"
    APPLICATION = "system/SIMOS/Application"
    ATTRIBUTE_TYPES = "system/SIMOS/AttributeTypes"
    BLOB = "system/SIMOS/Blob"
    DATASOURCE = "datasource"


class RoleCheckSupportedAuthProvider(str, Enum):
    AZURE_ACTIVE_DIRECTORY = "AAD"
