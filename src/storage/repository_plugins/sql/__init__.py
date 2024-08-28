import uuid
from fastapi.encoders import jsonable_encoder
from storage.repository_plugins.sql.models.blueprint_handling import SQLBlueprint, resolve_model
from sqlalchemy import create_engine, Column, String, Table, MetaData, text, select
from sqlalchemy.orm import sessionmaker,  aliased, selectinload
from storage.repository_interface import RepositoryInterface
import inspect as ins
from storage.repository_plugins.sql.models.base import Base



class Repository(RepositoryInterface):
    def __init__(
            self,
            username: str = "",
            password: str = "postgres",
            host: str = "",
            database: str = "",
            port: int = 5432,
            engine=None,
            **kwargs,
    ):

        password="postgres"
        if engine is None:
            # Default to PostgreSQL if engine is not provided
            print(username)
            print(password)
            print(port)
            print(host)
            print(database)
            self.engine = create_engine(
                f"postgresql://{username}:{password}@{host}:{port}/{database}",
                connect_args={"options": "-c statement_timeout=5000"}
            )
        else:
            self.engine = engine

        self.get_blueprint = kwargs['get_blueprint']
        self.Session = sessionmaker(bind=self.engine)()
        self.metadata = MetaData()
        self.table_ref = Table(
            "BP_Addresses",
            self.metadata,
            Column('Name', String),
            Column('Address',String),
        )
        self.table_content = Table(
            "content",
            self.metadata,
            Column('package_id', String),
            Column('index', String),
            Column('entity_id', String),
        )
        self.metadata.create_all(self.engine)


    def get(self,id,depth:int=0):
        entity=self.get_entity(id,depth)
        if entity['type']=="dmss://system/SIMOS/Package":
            entity['content']=self._get_content(id)
        return entity

    def get_entity(self, id: str,depth:int=0) -> dict:
        print('get is called')
        print(id)
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        allowed_tables = [i for i in metadata_obj.tables if
                          not (i.endswith("_map") or i.endswith("_value") or i == 'alembic_version' or i=="BP_Addresses" or i=='content' or i.endswith("_content"))]

        for table in allowed_tables:
            query = text(f'SELECT * FROM public."{table}" WHERE id = \'{id}\';')
            result = self.Session.execute(query).first()
            if result:
                query = text(f'SELECT "Address" FROM public."BP_Addresses" WHERE "Name" = \'{table}\';')
                address = session.execute(query).first()[0]
                if address:
                    model, bp = self._resolve_blueprint(address)
                    # Get top level data
                    parent_alias = aliased(model)
                    if depth<1:
                        # Fetches parent and all children to bottom
                        parent_alias = aliased(model)
                        result = (
                            session.query(model, parent_alias)
                            .filter(model.id == parent_alias.id)
                            .filter(model.id == id)
                            .options(selectinload('*'))
                        ).first()
                        result_dict = jsonable_encoder(result[0])
                        def remove_id_fields(d):
                            """Recursively remove `id` fields from a dictionary and convert 'value' lists to list of 'data' values."""
                            if isinstance(d, dict):
                                new_dict = {}
                                for k, v in d.items():
                                    if k == 'value' and isinstance(v, list):
                                        # Convert the 'value' list of dictionaries into a list of 'data' values
                                        new_dict[k] = [item.get('data') for item in v if isinstance(item, dict)]
                                    elif k != 'id':
                                        # Recursively handle other keys and values
                                        new_dict[k] = remove_id_fields(v)
                                return new_dict
                            elif isinstance(d, list):
                                # Apply the function to each item in the list
                                return [remove_id_fields(item) for item in d]
                            else:
                                return d

                        cleaned_result_dict = remove_id_fields(result_dict)
                        return (cleaned_result_dict)
                    top = (
                        session.query(model, parent_alias)
                        .filter(model.id == parent_alias.id)
                        .filter(model.id == id)
                    ).first()[0]
                    curr_level = 1
                    obj = [top]
                    while curr_level < depth:
                        for j in obj:
                            new_obj = []
                            for i in ins.getmembers(j):
                                if 'InstrumentedList' in type(i[1]).__name__:
                                    if len(i[1]) > 0:
                                        new_obj.extend(i[1])
                        curr_level += 1
                        obj = new_obj
                        if not obj:
                            break
                    return jsonable_encoder(obj)
                            # Resolve model from table

    def add(self,entity, id:str):
        a = self._verify_blueprint(entity)
        if not a:
            self.add_table(entity['type'])
        try:
            self.add_insert(entity, id=id)
            print(self.get(entity["type"]))
        except Exception as e:
            print(f"An error occurred: {e}")

        else:
            return jsonable_encoder(f"Entity not in database")

    def add_table(self, blueprint_address:str):
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        query = text(f'SELECT * FROM public."BP_Addresses" WHERE "Address" = \'{blueprint_address}\';')
        result = session.execute(query).first()
        if result:
            print(result)
            print(f"Blueprint already added to database")
            return jsonable_encoder(f"Blueprint already added to database")
        try:
            bp= self.get_blueprint.get_blueprint(blueprint_address).to_dict()
            bp = SQLBlueprint.from_dict(bp)
            bp.path=blueprint_address
            bp.paths = [[blueprint_address,bp.hash]]
            bp.generate_models_m2m_rel_with_paths(get_blueprint=self.get_blueprint)
            Base.metadata.create_all(self.engine)
            for i in range(len(bp.paths)):
                path,name = bp.paths[i][0], bp.paths[i][1]
                query = text('INSERT INTO public."BP_Addresses"("Name", "Address") VALUES (:name, :path);')
                query = query.bindparams(name=name, path=path)
                session.execute(query)
            session.commit()
            print(f"Blueprints:{bp.paths} succesfully added to database")
            return jsonable_encoder(f"Blueprints:{bp.paths} succesfully added to database")
        except Exception as e:
            print(f"An error occurred: {e}")
        return jsonable_encoder(f"Could not add blueprints to database")
    def add_insert(self, entity: dict, commit=True, id=None) -> dict:
        session=self.Session
        address = entity['type']
        model,bp = self._resolve_blueprint(address)
        data_table = {}
        children = []
        children_rel_names = []
        data = dict()
        for key, value in entity.items():

            if key == '_id':
                continue

            attr = [attr for attr in bp.attributes if attr.name == key][0]


            if attr.attributeType.lower() in ["string", "integer", "number", "float", "boolean", "foreign_key",
                                              "type", "core:blueprintattribute"]:
                if hasattr(attr, 'dimensions') and attr.dimensions == '*':
                    data_table[key] = value
                    print(data_table)
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
            child_obj = self.add_insert(child, commit=True,id=None)
            getattr(db_obj, rel_name).append(child_obj)

        for key, value in data_table.items():
            data_table_model = resolve_model(blueprint=bp,get_blueprint=self.get_blueprint,data_table_name=key)
            data_table_objects = [data_table_model(data=item) for item in value]
            getattr(db_obj, key).extend(data_table_objects)




        if 'type' in entity:
            db_obj.type = entity['type']

        if '_id' in entity:

            db_obj.id=entity['_id']
        session.add(db_obj)
        if commit:
            session.commit()
            session.refresh(db_obj)
        return db_obj
    def _add_content_from_package(self,content,package_id):
        """Adds the entities found in the content to the database and
        inserts the index and uid to content_table. This creates a mapping"""
        session = self.Session

        query = text('SELECT * FROM public."content" WHERE package_id = :package_id')
        result = session.execute(query, {'package_id': package_id})
        rows = result.fetchall()
        for entity_id in rows:
            self.delete(entity_id[-1])

        for index, entity in enumerate(content):
            # Generate a UUID for the entity
            entity_id = str(uuid.uuid4())
            self.add_table(entity['type'])
            entity['_id']=entity_id
            query = text(
                'DELETE FROM public."content" WHERE "package_id" = :package_id AND "index" = :index'
            )
            query = query.bindparams(package_id=package_id, index=str(index))
            session.execute(query)
            self.add_insert(entity, id=entity_id)
            # Insert into the content table
            query = text(
                'INSERT INTO public."content"("package_id", "index", entity_id) VALUES (:package_id, :index, :entity_id);')
            query = query.bindparams(package_id=package_id, index=index, entity_id=entity_id)
            session.execute(query)
        session.commit()

    def _get_content(self,package_id):
        session = self.Session
        content = []
        query = text('SELECT entity_id FROM content WHERE package_id = :package_id')
        result = session.execute(query, {'package_id': package_id})
        if result:
            for id in result:
                print(id)
                entity=self.get_entity(id[0])
                print(entity)
                content.append(entity)
        return content
    def _get_package(self, package_id):
        package=self.get(package_id)
        package['content']=self._get_content(package_id)
        return package


    def update(self,id:str,entity:dict):
        self.add_table("dmss://system/SIMOS/Package")
        if len(id[0])>1:
            id=id[0]

        session=self.Session
        query = text('SELECT * FROM public."_b1651397" WHERE id = :id')
        result = session.execute(query, {'id': id})
        rows = result.fetchall()
        if rows:
            self._add_content_from_package(entity['content'], id)
        elif entity['type']=="dmss://system/SIMOS/Package":
            content=entity['content']
            entity['content']=[]
            self.add_table(entity['type'])
            self.add_insert(entity,id)
            self._add_content_from_package(content, id)
        else:
            self._add_content_from_package([entity], id)

    def delete(self,id: str, table: str = None):
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        allowed_tables = [i for i in metadata_obj.tables if
                          not (i.endswith("_map") or i.endswith(
                              "_value") or i == 'alembic_version' or i == "BP_Addresses" or i=='content' or i.endswith('_content'))]
        try:
            for table in allowed_tables:

                query = text(
                    f'SELECT * FROM public."{table}" WHERE id = \'{id}\';'
                )
                result = self.Session.execute(query).first()
                if result:
                    query = text(f'SELECT "Address" FROM public."BP_Addresses" WHERE "Name" = \'{table}\';')
                    address = session.execute(query).first()[0]
                    if address:
                        model,bp=self._resolve_blueprint(address)
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
                        print(f"Successfully deleted {model.__name__}'{id}'")

        except Exception as e:
            print(f"An error occurred: {e}")
        return jsonable_encoder(f"Could not find id:{id} in database")
    def _resolve_blueprint(self,address):
        bp = self.get_blueprint.get_blueprint(address).to_dict()
        bp = SQLBlueprint.from_dict(bp)
        bp.path = address
        model = resolve_model(blueprint=bp,data_table_name=None,get_blueprint=self.get_blueprint)
        return model,bp
    def _verify_blueprint(self, entity:dict):
        type=entity['type']
        session = self.Session
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=self.engine)
        query = f'SELECT "Name" FROM public."BP_Addresses" WHERE "Address" = \'{type}\';'
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
    def find(self, filter: dict, single=None, raw=None) -> list[dict]:
        return []

    def find_one(self, filters: dict) -> dict:
        raise NotImplementedError


