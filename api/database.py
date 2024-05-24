from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from .settings import MariaSettings

maria_settings = MariaSettings()


DATABASE_URL = URL.create(
    drivername="mariadb+pymysql",
    username=maria_settings.username,
    password=maria_settings.password,
    host=maria_settings.host,
    port=maria_settings.port,
    database=maria_settings.database,
)

engine = create_engine(DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()