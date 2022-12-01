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
    BLUEPRINT = "sys://system/SIMOS/Blueprint"
    STORAGE_RECIPE = "sys://system/SIMOS/StorageRecipe"
    STORAGE_ATTRIBUTE = "sys://system/SIMOS/StorageAttribute"
    UI_RECIPE = "sys://system/SIMOS/UiRecipe"
    ENTITY = "sys://system/SIMOS/Entity"
    NAMED_ENTITY = "sys://system/SIMOS/NamedEntity"
    PACKAGE = "sys://system/SIMOS/Package"
    BLUEPRINT_ATTRIBUTE = "sys://system/SIMOS/BlueprintAttribute"
    ATTRIBUTE_TYPES = "sys://system/SIMOS/AttributeTypes"
    BLOB = "sys://system/SIMOS/Blob"
    RECIPE_LINK = "sys://system/SIMOS/RecipeLink"
    DATASOURCE = "datasource"


class AuthProviderForRoleCheck(str, Enum):
    AZURE_ACTIVE_DIRECTORY = "AAD"
