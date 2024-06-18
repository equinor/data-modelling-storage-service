from common.utils.logging import logger
from storage.repository_interface import RepositoryInterface
from


from sqlalchemy import create_engine, Column, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from time import sleep

class SQLClient(RepositoryInterface):
    def __init__(
        self,
        username :str= "postgres",
        password: str="postgres",
        host: str = "localhost",
        database: str = "simpos",
        table: str = "data_modelling",
        port: int = 5432,
        **kwargs,
    ):
        self.engine = create_engine(
            f"postgresql://{username}:{password}@{host}:{port}/{database}",
            connect_args={"options": "-c statement_timeout=5000"}
        )
        self.Session = sessionmaker(bind=self.engine)
        self.table = table
        self.metadata = MetaData(self.engine)
        #How should the reference table look like(internal, external, table_name)?
        self.table_ref = Table(
            self.table,
            self.metadata,
            Column('id', String, primary_key=True),
            Column('external_id'),
            Column('name', String)
        )
        self.metadata.create_all(self.engine)

    def get(self, uuid: str) -> dict:
        session = self.Session()
        attempts = 0
        while attempts < 50:
            attempts += 1
            try:
                #Query id and table from teble_ref, then use these to query
                query =  session.query(table_ref.external_id).filter(table_ref.id == uuid).one_or_none()[0]
            except IntegrityError as ex:
                raise NotFoundException(uid)
            try:
                id = query.id
                table = query.table
                return session.query(table).filter(table.id == id).one_or_none()._asdict()
            except IntegrityError as ex:
                raise NotFoundException(uid)
            except SQLAlchemyError as ex:
                session.rollback()
                sleep(3)
                if attempts > 2:
                    raise ex
            finally:
                session.close()

    def add(self, uid: str, document: dict) -> bool:
        session = self.Session()

        try:

            session.execute(
                self.table_ref.insert().values(id=uid, data=str(document))
            )
            session.commit()
            return True
        except IntegrityError as ex:
            session.rollback()
            raise BadRequestException from ex
        except SQLAlchemyError as ex:
            session.rollback()
            raise ex
        finally:
            session.close()



    def update(self, uid: str, document: dict, **kwargs) -> bool:
        session = self.Session()
        attempts = 0
        while attempts < 50:
            attempts += 1
            try:
                result = session.execute(
                    self.table_ref.update().where(self.table_ref.c.id == uid).values(data=str(document))
                )
                session.commit()
                if result.rowcount == 0:
                    raise NotFoundException(uid)
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                sleep(3)
                if attempts > 2:
                    raise ex
            finally:
                session.close()
    def find(self, filters: dict) -> list[dict] | None:
        pass



