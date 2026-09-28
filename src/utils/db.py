from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.utils.settings import Settings

Base=declarative_base()

engine=create_engine(url=Settings.db_connection)

localsession=sessionmaker(bind=engine)

def get_db():
    session=localsession()
    try:
        yield session
    finally:
        session.close()