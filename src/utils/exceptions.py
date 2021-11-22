from fastapi import HTTPException
from starlette import status


class RepositoryException(Exception):
    def __init__(self, message: str):
        super()
        self.message = message

    def __str__(self):
        return self.message


class EntityAlreadyExistsException(RepositoryException):
    def __init__(self, document_id=None, message: str = None):
        super().__init__(message=f"The document with id '{document_id}' already exists" if not message else message)


class EntityNotFoundException(RepositoryException):
    def __init__(self, uid, message: str = None):
        if message:
            super().__init__(message=message)
        else:
            super().__init__(message=f"The entity, with id {uid} is not found")


class DataSourceNotFoundException(RepositoryException):
    def __init__(self, uid):
        super().__init__(message=f"The data source, with id '{uid}' is not found")


class DataSourceAlreadyExistsException(RepositoryException):
    def __init__(self, uid):
        super().__init__(message=f"The data source, with id '{uid}' already exists")


class InvalidSortByAttributeException(RepositoryException):
    def __init__(self, sort_by_attribute, type):
        super().__init__(message=f"'{sort_by_attribute}' is not a valid attribute in the '{type}'")


class BadRequestException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidEntityException(RepositoryException):
    def __init__(self, message):
        super().__init__(message=message)


class InvalidBlueprintException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDocumentNameException(RepositoryException):
    def __init__(self, name):
        super().__init__(
            message=f"'{name}' is a invalid document name. "
            f"Only alphanumeric, underscore, and dash are allowed characters"
        )


class InvalidAttributeException(RepositoryException):
    def __init__(self, attribute_name, type):
        super().__init__(message=f"'{attribute_name}' is not a valid attribute in the '{type}'")


class RootPackageNotFoundException(Exception):
    def __init__(self, data_source_id=None, file=None):
        self.data_source_id = data_source_id if data_source_id else None
        self.file = file if file else None

    def __str__(self):
        if self.data_source_id and self.file:
            return f"No root package with name '{self.file}', in data source '{self.data_source_id}' could be found."
        else:
            return "The root package could not be found"


class FileNotFoundException(Exception):
    def __init__(self, data_source_id=None, file=None):
        self.data_source_id = data_source_id if data_source_id else None
        self.file = file if file else None

    def __str__(self):
        if self.data_source_id and self.file:
            return f"No file with name '{self.file}', in data source '{self.data_source_id}' could be found."
        else:
            return "The file could not be found in the data source"


class DuplicateFileNameException(Exception):
    def __init__(self, data_source_id=None, path=None):
        self.data_source_id = data_source_id if data_source_id else None
        self.path = path if path else None

    def __str__(self):
        if self.data_source_id and self.path:
            return f"'{self.data_source_id}/{self.path}' already exists"
        else:
            return (
                "Can't create the requested document, one with the same name within the same package already exists."
            )


class InvalidChildTypeException(Exception):
    def __init__(self, invalid_type, key, valid_type):
        super().__init__(
            f"The type '{invalid_type}' is not a valid type for the "
            f"'{key}' attribute. The type should be of type '{valid_type} (or extending from it)'"
        )


class ImportException(Exception):
    def __init__(self, message=None):
        self.message = message if message else "Something went wrong during the import"


class InvalidDataSourceException(Exception):
    def __init__(self, message=None):
        self.message = message if message else "The data source is invalid"


class MissingPrivilegeException(Exception):
    def __init__(self, message=None):
        self.message = message if message else "Missing privileges to perform operation on the resource"


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed", headers={"WWW-Authenticate": "Bearer"}
)


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message if message else "Could not validate the content"
