from email.policy import default
from sqlalchemy import Column, DateTime,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

def mydefault(context):
    return context.get_current_parameters()['email']

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    first_name = Column(String,default=mydefault)
    last_name = Column(String)
    bio = Column(String)
    phone_number = Column(Integer)
    email = Column(String,unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    

