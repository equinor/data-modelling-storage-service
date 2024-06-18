from uuid import uuid4
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, text
import re

"""
SQLAlchemy base model
"""


class ExtendedBaseModel(object):
    """
    Base for all database models.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Sets the SQL table name equal to the class name
        """
        return cls.__name__

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False,
                server_default=text("uuid_generate_v4()"))


# The common source for all future SQLAlchemy classes
Base = declarative_base(cls=ExtendedBaseModel)
