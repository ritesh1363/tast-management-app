from sqlalchemy import Column,String,Integer,Boolean,DateTime
from src.utils.db import Base

class user_model(Base):
    __tablename__="usertable"

    id=Column(Integer,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    hash_password=Column(String,nullable=False)
    email=Column(String)

