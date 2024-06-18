from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional, TypeVar, Type
from alembic.config import Config
from alembic import command
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.ext.orderinglist import ordering_list
import os
from datetime import datetime
from sqlalchemy.sql import text

from .base import Base

"""
Provides the declarative base for all the custom models
"""

alembic_cfg = Config('alembic.ini')  # Provide the path to your alembic.ini file

type_mapping = {
    "string": String,
    "integer": Integer,
    "number": Float,
    "float": Float,
    "boolean": Boolean,
    "foreign_key": ForeignKey,
    'type': String,
    'core:blueprintattribute': String
}


class Attribute(BaseModel):
    name: str
    type: str
    label: Optional[str] = None
    attributeType: str
    dimensions: Optional[str] = None
    contained: Optional[bool] = None
    optional: Optional[bool] = True


class Blueprint(BaseModel):
    name: str
    type: str
    description: str
    attributes: Optional[List[Attribute]] = None
    path: str = None
    contained: bool = False
    @classmethod
    def from_json(cls, file):
        relative_path = f'{file}.blueprint.json'
        try:
            with open(relative_path, "r") as json_file:
                json_data = json_file.read()
        except FileNotFoundError:
            return None

        blueprint = Blueprint.model_validate_json(json_data)
        blueprint.path = relative_path
        return blueprint

    def generate_models_m2m_rel(self, parent: str = None, parent_contained: bool = False):
        class_attributes = {}
        children = []
        data_tables = []
        for attr in self.attributes:
            attr_name = attr.name
            if attr_name == 'type':  # no need to store the blueprint type in the database
                continue
            attr_type = attr.attributeType.lower()  # Convert type to lowercase for mapping

            if type_mapping.get(attr_type) and hasattr(attr, 'dimensions') and attr.dimensions == '*':
                # treat this as one-to-many exclusively
                sqlalchemy_data_tale_column_type = type_mapping.get(attr_type)

                if attr.contained:
                    on_delete = 'cascade'
                else:
                    on_delete = None

                data_tables.append({
                    'name': f'{self.name}_{attr_name}',
                    'columns': {
                        f'{self.name}_id': Column(f'{self.name}_id',
                                                  ForeignKey(f'{self.name}.id', ondelete=on_delete),
                                                  primary_key=True, nullable=False, info={"skip_pk": True}),
                        'index': Column(Integer, nullable=False, primary_key=True, info={"skip_pk": True}),
                        'data': Column(sqlalchemy_data_tale_column_type, nullable=False),
                        'id': None
                    }
                })
                class_attributes[attr_name] = relationship(f'{self.name}_{attr_name}',
                                                           order_by=f'{self.name}_{attr_name}.index',
                                                           collection_class=ordering_list('index'),
                                                           cascade="all, delete" if (attr.contained or parent_contained) else "save-update")

            elif type_mapping.get(attr_type):  # Should be made to catch any type that is not a blueprint
                sqlalchemy_column_type = type_mapping.get(attr_type)
                class_attributes[attr_name] = Column(sqlalchemy_column_type, nullable=attr.optional)
            else:  # add paths to json-blueprints for children
                file = os.path.normpath(os.path.join(os.path.dirname(self.path), attr_type))
                child_blueprint = self.from_json(file)
                if attr.contained:
                    child_blueprint.contained = True
                children.append(child_blueprint)
                child_name = child_blueprint.name
                class_attributes[f'{attr_name}'] = relationship(child_name,
                                                                   secondary=f'{self.name}_{child_name}_map',
                                                                   cascade="all, delete" if (attr.contained or parent_contained) else "save-update")
        if parent:
            table_name = f"{parent}_{self.name}_map"
            if table_name in globals():
                existing_cols = [c.name for c in globals()[table_name].columns]
                if f"{parent}_id" not in existing_cols or f"{self.name}_id" not in existing_cols:
                    raise ValueError(f'Association table "{table_name}" already exists, but does not correspond to '
                                     f'existing version of "{self.name}"')
            else:
                globals()[table_name] = Table(
                    table_name,
                    Base.metadata,
                    Column(f"{parent}_id",
                           ForeignKey(f"{parent}.id")),
                    Column(f"{self.name}_id",
                           ForeignKey(f"{self.name}.id")),
                )

        if self.name in globals():
            for attr in self.attributes:
                attr_name = attr.name
                if attr_name == 'type':
                    continue
                attr_type = attr.attributeType.lower()
                if type_mapping.get(attr_type):
                    if not getattr(globals()[self.name], attr_name):
                        raise ValueError(f'Attribute "{attr_name}" not found in existing version of "{self.name}"')
        else:
            globals()[self.name] = type(self.name, (Base,), class_attributes)
            for data_table in data_tables:
                globals()[data_table['name']] = type(data_table['name'], (Base,), data_table['columns'])

        for child_blueprint in children:
            child_blueprint.generate_models_m2m_rel(parent=self.name, parent_contained=child_blueprint.contained)

    def migrate_and_upgrade(self):
        command.revision(alembic_cfg, autogenerate=True, message=f'table_{self.name}')
        command.upgrade(alembic_cfg, revision='head')

    def return_model(self):
        if self.name in globals():
            return globals()[self.name]
        else:
            return None

    def return_data_table_model(self, name: str):
        if f'{self.name}_{name}' in globals():
            return globals()[f'{self.name}_{name}']
        else:
            return None


class Blueprints(BaseModel):
    bps: List[Blueprint] = []

    def append(self, bp: Blueprint):
        self.bps.append(bp)

    def __len__(self):
        return len(self.bps)

    def __getitem__(self, item):
        return self.bps[item]

    def __iter__(self):
        return iter(self.bps)

    def generate_models(self):
        for blueprint in self.bps:
            blueprint.generate_models_m2m_rel()

    @staticmethod
    def generate_migration_script(message: str = f'models: {datetime.now().strftime("%Y-%m-%d")}'):
        revision = command.revision(alembic_cfg, autogenerate=True, message=message)
        return revision.revision

    @staticmethod
    def upgrade(revision='head'):
        command.upgrade(alembic_cfg, revision=revision)


ModelType = TypeVar("ModelType", bound=Base)


def resolve_blueprint(entity_type: str) -> Blueprint:
    blueprint_path = entity_type.split(':')[1]
    base_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
    return Blueprint.from_json(os.path.join(base_path, blueprint_path))


def resolve_model(blueprint: Blueprint, data_table_name: str = None) -> Type[ModelType]:
    if not data_table_name:
        if not blueprint.return_model():
            blueprint.generate_models_m2m_rel()

        return blueprint.return_model()
    else:
        if not blueprint.return_data_table_model(data_table_name):
            blueprint.generate_models_m2m_rel()

        return blueprint.return_data_table_model(data_table_name)
