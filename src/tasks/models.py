from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from src.utils.db import Base
from src.users.models import user_model

class taskmodel(Base):
    __tablename__="user_tasks"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    is_completed=Column(Boolean,default=False)

    user_id=Column(Integer,ForeignKey("usertable.id",ondelete="CASCADE"))
