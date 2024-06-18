from pydantic import Field
from typing import List
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Application configuration
    """
    SQLALCHEMY_DATABASE_URI: str = Field('', validation_alias='SQLALCHEMY_DATABASE_URI')
