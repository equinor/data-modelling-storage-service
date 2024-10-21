from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

"""
SQLAlchemy base model
"""


class ExtendedBaseModel:
    """
    Base for all database models.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Sets the SQL table name equal to the class name
        """
        return cls.__name__  # type: ignore

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False)


# The common source for all future SQLAlchemy classes
Base = declarative_base(cls=ExtendedBaseModel)
