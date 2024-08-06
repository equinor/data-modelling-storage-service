import uuid
from fastapi.encoders import jsonable_encoder
from storage.repositories.plugin.sql.models.blueprint_handling import SQLBlueprint, resolve_model
from sqlalchemy import create_engine, Column, String, Table, MetaData, text
from sqlalchemy.orm import sessionmaker,  aliased, selectinload
from common.providers.blueprint_provider import default_blueprint_provider
from storage.repository_interface import RepositoryInterface
from common.exceptions import NotFoundException
from alembic.config import Config
class SQLClient(RepositoryInterface):
    def __init__(
            self,
            username: str = "postgres",
            password: str = "postgres",
            host: str = "localhost",
            database: str = "dmss",
            table: str = "BP_Addresses",
            port: int = 5432,
            engine=None,
            alembic_cfg:Config = Config(
                r'C:\Users\jta\OneDrive - SevanSSP AS\Desktop\equinor_fork\data-modelling-storage-service\src\storage\repositories\plugin\sql\alembic.ini'),
            **kwargs,
    ):
        if engine is None:
            # Default to PostgreSQL if engine is not provided
            self.engine = create_engine(
                f"postgresql://{username}:{password}@{host}:{port}/{database}",
                connect_args={"options": "-c statement_timeout=5000"}
            )
        else:
            # Use the provided engine (assuming it's already configured)
            self.engine = engine

        self.Session = sessionmaker(bind=self.engine)()
        self.table = table
        self.metadata = MetaData()
        self.table_ref = Table(
            self.table,
            self.metadata,
            Column('Name', String),
            Column('Address',String),
        )
        self.metadata.create_all(self.engine)
        self.alembic_cfg=alembic_cfg

    def get(self, id: str,all_data=bool,levels:int=1) -> dict:
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        allowed_tables = [i for i in metadata_obj.tables if
                          not (i.endswith("_map") or i.endswith("_value") or i == 'alembic_version' or i=="BP_Addresses")]
        result=None
        for table in allowed_tables:
            query = text(f'SELECT * FROM public."{table}" WHERE id = \'{id}\';')
            result = self.Session.execute(query).first()
            if result:
                query = f'SELECT "Address" FROM public."BP_Addresses" WHERE "Name" = \'{table}\';'
                address = session.execute(query).first()[0]
                if address:
                    model, bp = self._resolve_blueprint(address)
                    # Get top level data
                    parent_alias = aliased(model)
                    if all_data:
                        # Fetches parent and all children to bottom
                        parent_alias = aliased(model)
                        return jsonable_encoder((
                                                    session.query(model, parent_alias)
                                                    .filter(model.id == parent_alias.id)
                                                    .filter(model.id == id)
                                                    .options(selectinload('*'))
                                                ).first()[0])

                        # Fetches only parent
                    top = (
                        session.query(model, parent_alias)
                        .filter(model.id == parent_alias.id)
                        .filter(model.id == uuid)
                    ).first()[0]

                    # Iterate trough levels to fetch nested children
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
        return jsonable_encoder(f"Could not find id:{id} in database")
                            # Resolve model from table

    def add(self,entity, id:str):
        a=self._verify_blueprint(entity)
        if a:
            try:
                self.add_insert(entity,id=id)
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            return jsonable_encoder(f"Entity not in database")

    def add_table(self, blueprint_address:str):
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        query = f'SELECT * FROM public."BP_Addresses" WHERE "Address" = \'{blueprint_address}\';'
        result = session.execute(query).first()[0]
        if result:
            return jsonable_encoder(f"Blueprint already added to database")
        try:
            bp = default_blueprint_provider.get_blueprint(blueprint_address).to_dict()
            bp = SQLBlueprint.from_dict(bp)
            bp.path = blueprint_address
            bp.paths = [blueprint_address]
            bp.generate_models_m2m_rel_with_paths()
            bp.generate_migration_script(alembic_cfg=self.alembic_cfg)
            bp.upgrade(alembic_cfg=self.alembic_cfg)
            for path in bp.paths:
                name = path.split('/')[-1]
                query = f'INSERT INTO public."BP_Addresses"("Name", "Address") VALUES (\'{name}\', \'{path}\');'
                session.execute(query)
            session.commit()
            return jsonable_encoder(f"Blueprints:{bp.paths} succesfully added to database")
        except Exception as e:
            print(f"An error occurred: {e}")
        return jsonable_encoder(f"Could not add blueprints to database")



    def add_insert(self, entity: dict, commit=True, id=None) -> dict:
        session=self.Session
        table=entity['type'].split('/')[-1]
        query = f'SELECT "Address" FROM public."BP_Addresses" WHERE "Name" = \'{table}\';'
        address = session.execute(query).first()[0]
        model,bp = self._resolve_blueprint(address)
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
            child_obj = self.add_insert(child, commit=True)
            getattr(db_obj, rel_name).append(child_obj)


        for key, value in data_table.items():
            data_table_model = resolve_model(bp, key)
            data_table_objects = [data_table_model(data=item) for item in value]
            getattr(db_obj, key).extend(data_table_objects)

        if id:
            db_obj.id=id
        session.add(db_obj)
        if commit:
            session.commit()
            session.refresh(db_obj)
        return db_obj
    def update(self,id:str,entity:dict):
        try:
            self.delete(id=id)
            self.add_insert(entity,id=id)
        except Exception as e:
            print(f"An error occurred: {e}")




    def update_table(self, id:str,document:dict):
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        allowed_tables = [i for i in metadata_obj.tables if
                          not (i.endswith("_map") or i.endswith(
                              "_value") or i == 'alembic_version' or i == 'BP_Addresses')]
        try:
            for table in allowed_tables:
                query = text(
                    f'SELECT * FROM public."{table}" WHERE id = \'{id}\';'
                )
                result = self.Session.execute(query).first()
                if result:
                    try:
                        set_clause = ", ".join([f'"{key}" = {document[key]}' for key in document.keys() if key != 'id'])
                        query = text(f'UPDATE public."{table}" SET {set_clause} WHERE id = \'{id}\';')
                        session.execute(query)
                        session.commit()
                    except Exception as e:
                        print(f"An error occurred: {e}")
        except NotFoundException as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            session.close()
        return jsonable_encoder(f"Could not update:{id} in database")

    def delete(self,id: str, table: str = None):
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        allowed_tables = [i for i in metadata_obj.tables if
                          not (i.endswith("_map") or i.endswith(
                              "_value") or i == 'alembic_version' or i == "BP_Addresses")]
        try:
            for table in allowed_tables:
                query = text(
                    f'SELECT * FROM public."{table}" WHERE id = \'{id}\';'
                )
                result = self.Session.execute(query).first()
                if result:
                    query = f'SELECT "Address" FROM public."BP_Addresses" WHERE "Name" = \'{table}\';'
                    address = session.execute(query).first()[0]

                    if address:
                        model,bp=self._resolve_blueprint(address)
                        # Get top level data
                        obj = self.Session.query(model).get(id)
                        parent_mapping_tables = [i for i in metadata_obj.tables if (i.endswith(f"{table}_map"))]
                        for j in parent_mapping_tables:
                            query = text(
                                f'delete FROM public."{j}" WHERE "{table}_id" = \'{id}\';'
                            )
                            self.Session.execute(query)
                            self.Session.commit()
                        self.Session.delete(obj)
                        self.Session.flush()
                        self.Session.commit()
                        return jsonable_encoder(f"Successfully deleted {model.__name__}'{id}'")
        except Exception as e:
            print(f"An error occurred: {e}")
        return jsonable_encoder(f"Could not find id:{id} in database")
    def _resolve_blueprint(self,address):
        bp = default_blueprint_provider.get_blueprint(address).to_dict()
        bp = SQLBlueprint.from_dict(bp)
        bp.path = address
        model = resolve_model(bp)
        return model,bp
    def _verify_blueprint(self, entity:dict):
        type=entity['type'].rsplit('/',1)[-1]
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        query = f'SELECT "Name" FROM public."BP_Addresses" WHERE "Name" = \'{type}\';'
        table = session.execute(query).first()
        if table:
            return True
        return False
    def get_blob(self, uid):
        raise NotImplementedError

    def delete_blob(self, uid: str):
        raise NotImplementedError

    def update_blob(self, uid: str, blob: bytearray):
        raise NotImplementedError
    def find(self, filter: dict, single=None, raw=None) -> dict:
        return self.get(filter["type"])

    def find_one(self, filters: dict) -> dict:
        raise NotImplementedError


