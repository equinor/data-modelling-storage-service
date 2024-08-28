from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional, TypeVar, Type
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.ext.orderinglist import ordering_list
from .base import Base
import hashlib


"""
Provides the declarative base for all the custom models
"""


type_mapping = {
    "string": String,
    "integer": Integer,
    "number": Float,
    "float": Float,
    "boolean": Boolean,
    "foreign_key": ForeignKey,
    'type': String,
    "object":String,
    'core:blueprintattribute': String,
    '_meta_':String
}


class Attribute(BaseModel):
    name: str
    type: str
    label: Optional[str] = None
    attributeType: str
    dimensions: Optional[str] = None
    contained: Optional[bool] = None
    optional: Optional[bool] = True

class SQLBlueprint(BaseModel):
    name: str
    type: str
    description: str
    attributes: Optional[List[Attribute]] = None
    _path: str = None
    hash: str = None
    contained: bool = False
    paths:List[List[str]]=None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        self._path = value
        self.hash = self.generate_hash(value)

    def generate_hash(self, path: str, length: int = 8) -> str:
        # Generate a SHA-256 hash and truncate it to the desired length
        full_hash = hashlib.sha256(path.encode()).hexdigest()
        return '_'+full_hash[:length]


    @classmethod
    def from_json(cls, file):
        relative_path = f'{file}.blueprint.json'
        try:
            with open(relative_path, "r") as json_file:
                json_data = json_file.read()
        except FileNotFoundError:
            return None

        blueprint = SQLBlueprint.model_validate_json(json_data)
        blueprint.path = relative_path
        return blueprint

    @classmethod
    def from_dict(cls, adict):
        instance = cls(**adict)
        return instance

    def generate_models_m2m_rel(self, get_blueprint,parent: str = None, parent_contained: bool = False):
        self.name=self.hash
        class_attributes = {}
        children = []
        data_tables = []

        for attr in self.attributes:
            attr_name = attr.name


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

                address=attr.attributeType
                bp = get_blueprint.get_blueprint(address).to_dict()

                child_blueprint = SQLBlueprint.from_dict(bp)

                child_blueprint.path = address
                child_blueprint.name=child_blueprint.hash


                if attr.contained:
                    child_blueprint.contained = True
                children.append(child_blueprint)
                child_name = child_blueprint.name
                class_attributes[f'{attr_name}'] = relationship(child_name,
                                                                   secondary=f'{self.hash}_{child_name}_map',
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
                attr_type = attr.attributeType.lower()
                if type_mapping.get(attr_type):
                    if not getattr(globals()[self.name], attr_name):
                        raise ValueError(f'Attribute "{attr_name}" not found in existing version of "{self.name}"')
        else:

            globals()[self.name] = type(self.name, (Base,), class_attributes)
            for data_table in data_tables:
                globals()[data_table['name']] = type(data_table['name'], (Base,), data_table['columns'])

        for child_blueprint in children:
            child_blueprint.generate_models_m2m_rel(get_blueprint=get_blueprint,parent=self.name, parent_contained=child_blueprint.contained)

    def generate_models_m2m_rel_with_paths(self,get_blueprint, parent: str = None, parent_contained: bool = False,bp_root=None):
        self.name = self.hash
        class_attributes = {}
        children = []
        data_tables = []
        if not bp_root:
            bp_root=self
        for attr in self.attributes:
            attr_name = attr.name
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

                address = attr.attributeType
                bp = get_blueprint.get_blueprint(address).to_dict()
                child_blueprint = SQLBlueprint.from_dict(bp)
                child_blueprint.paths=[]
                child_blueprint.path = address
                child_blueprint.name=child_blueprint.hash
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

                attr_type = attr.attributeType.lower()
                if type_mapping.get(attr_type):
                    if not getattr(globals()[self.name], attr_name):
                        raise ValueError(f'Attribute "{attr_name}" not found in existing version of "{self.name}"')
        else:
            globals()[self.name] = type(self.name, (Base,), class_attributes)
            for data_table in data_tables:
                globals()[data_table['name']] = type(data_table['name'], (Base,), data_table['columns'])

        for child_blueprint in children:
            child_blueprint.generate_models_m2m_rel_with_paths(get_blueprint=get_blueprint,parent=self.name, parent_contained=child_blueprint.contained,bp_root=bp_root)
            bp_root.paths.append([child_blueprint.path,child_blueprint.hash])

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

ModelType = TypeVar("ModelType", bound=Base)


def resolve_model(blueprint: SQLBlueprint,get_blueprint=None, data_table_name: str = None) -> Type[ModelType]:
    if not data_table_name:
        if not blueprint.return_model():
            blueprint.generate_models_m2m_rel(get_blueprint=get_blueprint)
        return blueprint.return_model()
    else:
        if not blueprint.return_data_table_model(data_table_name):
            blueprint.generate_models_m2m_rel(get_blueprint=get_blueprint)
        return blueprint.return_data_table_model(data_table_name)
