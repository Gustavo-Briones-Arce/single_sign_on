from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config.setting import setting

SERVER = setting.SQL_HOST
PORT = setting.SQL_PORT
USER = setting.SQL_USER
PASSWORD = setting.SQL_PASSWORD
DB = setting.SQL_DB
SQL_URL = f'postgresql+psycopg2://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}'

# connect_args = {"check_same_thread": False}
engine = create_engine(SQL_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False)
Base = declarative_base()


def get_new_uuid():
    return str(uuid4())

#TODO create class when extends base with id, on_created and on_updated
