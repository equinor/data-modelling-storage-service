from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_session
from typing import Any
from uuid import UUID
from sqlalchemy import MetaData, Table
from plugin.models import Blueprint, resolve_model
from fastapi.encoders import jsonable_encoder
import os
from sqlalchemy import text
from sqlalchemy.orm import aliased, selectinload
import inspect

router = APIRouter()


@router.get('/{id}', response_model=Any)
def get_data_by_id(id: UUID, table: str = None, levels: int = 1, all_data: bool = False,
                   session: Session = Depends(get_db_session)):
    engine = session.get_bind()
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)

    allowed_tables = [i for i in metadata_obj.tables if
                      not (i.endswith("_map") or i.endswith("_value") or i == 'alembic_version')]
    if table:
        if table not in allowed_tables:
            raise HTTPException(status_code=404, detail=f"Could not find table {table}")
        else:
            allowed_tables = [table]

    for table in allowed_tables:
        query = text(
            f'SELECT * FROM public."{table}" WHERE id = \'{id}\';'
        )
        result = session.execute(query).first()
        if result:
            for root, _, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'models')):

                if f'{table}.blueprint.json' in files:
                    # Resolve model from table
                    bp = Blueprint.from_json(os.path.join(root, table))
                    model = resolve_model(bp)

                    # Get top level data
                    parent_alias = aliased(model)
                    if all_data:
                        #Fetches parent and all children to bottom
                        parent_alias = aliased(model)
                        return jsonable_encoder((
                                                    session.query(model, parent_alias)
                                                    .filter(model.id == parent_alias.id)
                                                    .filter(model.id == id)
                                                    .options(selectinload('*'))
                                                ).first()[0])

                        #Fetches only parent
                    top = (
                        session.query(model, parent_alias)
                        .filter(model.id == parent_alias.id)
                        .filter(model.id == id)
                    ).first()[0]

                        #Iterate trough levels to fetch nested children
                    curr_level = 1
                    obj = [top]
                    while curr_level < levels:
                        for j in obj:
                            new_obj = []
                            for i in inspect.getmembers(j):
                                if 'InstrumentedList' in type(i[1]).__name__:
                                    if len(i[1]) > 0:
                                        new_obj.extend(i[1])
                        curr_level += 1
                        obj = new_obj
                        if not obj:
                            break
                    return jsonable_encoder(top)
    raise HTTPException(status_code=404, detail=f"Could not find ID {id}")


@router.post('/', response_model=Any)
def create_entity(entity: dict, return_all: bool = False, session: Session = Depends(get_db_session)):
    def create_entity_recursive(entity, is_toplevel, session):
        try:
            table = entity['type'].rsplit('/')[1]
        except AttributeError:
            HTTPException(status_code=400, detail=f"Invalid input, BP should be available as attribute: type")
        for root, _, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'models')):
            if f'{table}.blueprint.json' in files:
                # Resolve model from table
                bp = Blueprint.from_json(os.path.join(root, table))
                model = resolve_model(bp)

                data_table = {}
                children = []
                children_rel_names = []
                data = dict()
                for key, value in entity.items():
                    attr = [attr for attr in bp.attributes if attr.name == key][0]
                    if attr.name == 'type':
                        continue
                    if attr.attributeType.lower() in ["string", "integer", "number", "float", "boolean", "foreign_key", "type",
                                                      "core:blueprintattribute"]:
                        if hasattr(attr, 'dimensions') and attr.dimensions == '*':
                            data_table[key] = value
                        else:
                            data[key] = value
                    else:
                        if isinstance(value, list):
                            children.extend(value)
                            [children_rel_names.append(key) for _ in value]
                        elif isinstance(value, dict):
                            children.append(value)
                            children_rel_names.append(key)
                        else:
                            raise NotImplementedError(f'Type {type(value)} not supported yet')

                obj_in_data = jsonable_encoder(data)
                db_obj = model(**obj_in_data)
                for child, rel_name in zip(children, children_rel_names):
                    child_obj = create_entity_recursive(child, False, session)
                    getattr(db_obj, rel_name).append(child_obj)

                for key, value in data_table.items():
                    data_table_model = resolve_model(bp, key)
                    data_table_objects = [data_table_model(data=item) for item in value]
                    getattr(db_obj, key).extend(data_table_objects)

                session.add(db_obj)
                session.commit()
                session.refresh(db_obj)
                if is_toplevel:
                    return jsonable_encoder(db_obj)
                else:
                    return db_obj

            HTTPException(status_code=404, detail=f"Could not find Blueprint {table}")
    new_obj = create_entity_recursive(entity, True, session)
    #Re-use get_endpoint to fetch all nested objects
    if return_all:
        new_id = new_obj['id']
        return get_data_by_id(id=new_id, all_data=True, session=session)
    return new_obj


@router.delete('/{id}', response_model=Any)
def delete_data_by_id(id: UUID, table: str = None,
                   session: Session = Depends(get_db_session)):
    engine = session.get_bind()
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)

    allowed_tables = [i for i in metadata_obj.tables if
                      not (i.endswith("_map") or i.endswith("_value") or i == 'alembic_version')]
    if table:
        if table not in allowed_tables:
            raise HTTPException(status_code=404, detail=f"Could not find table {table}")
        else:
            allowed_tables = [table]

    for table in allowed_tables:
        query = text(
            f'SELECT * FROM public."{table}" WHERE id = \'{id}\';'
        )
        result = session.execute(query).first()
        if result:
            for root, _, files in os.walk(os.path.join(os.path.dirname(__file__), '..', 'models')):

                if f'{table}.blueprint.json' in files:
                    # Resolve model from table
                    bp = Blueprint.from_json(os.path.join(root, table))
                    model = resolve_model(bp)

                    # Get top level data
                    obj = session.query(model).get(id)
                    session.delete(obj)
                    session.commit()
                    session.flush()
                    return jsonable_encoder(f"Successfully deleted {model.__name__}'{id}'")
    raise HTTPException(status_code=404, detail=f"Could not find ID {id}")
