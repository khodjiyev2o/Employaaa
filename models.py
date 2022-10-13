from typing import Dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,)
    last_name = Column(String)
    phone_number = Column(Integer)
    email = Column(String,)
    photo = Column()#No idea what to put here,i made pydantic submodel in schema.py with Image class for this attribute. 
    
