from sqlalchemy import Column, DateTime,Integer, String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func



Base = declarative_base()

class Company(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    owner_id  = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    
companies=Company.__table__