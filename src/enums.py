from enum import Enum

PRIMITIVES = {"string", "number", "integer", "boolean"}


class Protocols(Enum):
    DMSS = "dmss"


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
    BLUEPRINT = "dmss://system/SIMOS/Blueprint"
    STORAGE_RECIPE = "dmss://system/SIMOS/StorageRecipe"
    STORAGE_ATTRIBUTE = "dmss://system/SIMOS/StorageAttribute"
    UI_RECIPE = "dmss://system/SIMOS/UiRecipe"
    UI_ATTRIBUTE = "dmss://system/SIMOS/UiAttribute"
    ENTITY = "dmss://system/SIMOS/Entity"
    NAMED_ENTITY = "dmss://system/SIMOS/NamedEntity"
    PACKAGE = "dmss://system/SIMOS/Package"
    BLUEPRINT_ATTRIBUTE = "dmss://system/SIMOS/BlueprintAttribute"
    ATTRIBUTE_TYPES = "dmss://system/SIMOS/AttributeTypes"
    BLOB = "dmss://system/SIMOS/Blob"
    RECIPE_LINK = "dmss://system/SIMOS/RecipeLink"
    DATASOURCE = "datasource"
    REFERENCE = "dmss://system/SIMOS/Reference"


class REFERENCE_TYPES(Enum):
    LINK = "link"
    POINTER = "pointer"
    STORAGE = "storage"


class AuthProviderForRoleCheck(str, Enum):
    AZURE_ACTIVE_DIRECTORY = "AAD"
