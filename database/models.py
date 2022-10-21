from sqlalchemy import Column, DateTime,Integer, String,ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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




class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    owner_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"),nullable=False)
    name = Column(String,unique=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    visible = Column(Boolean, server_default='TRUE')


companies=Company.__table__