from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import Config
from plugin import models

engine = None


def get_db_session():
    """
    Create an independent database session/connection per request. Use the same session through all the request and
    then close it after the request is finished.
    """
    config = Config()
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, executemany_mode="values_plus_batch")
    models.Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        return session
