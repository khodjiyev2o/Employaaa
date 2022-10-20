from sqlalchemy import Column, DateTime,Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    first_name = Column(String,)
    last_name = Column(String)
    bio = Column(String)
    phone_number = Column(Integer)
    email = Column(String,unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    
users=User.__table__