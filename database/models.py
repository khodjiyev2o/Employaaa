from email.mime import application
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
    invite = relationship("Invite",back_populates='user')



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
    application = relationship("Invite",back_populates='company')
    members = relationship("Member",back_populates='company')

companies=Company.__table__


class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_admin = Column(Boolean, server_default='FALSE')

    company_id = Column(Integer, ForeignKey("companies.id"))


    company = relationship("Company",back_populates='members')


members=Member.__table__



class Invite(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))


    company = relationship("Company",back_populates='application')
    user = relationship("User",back_populates='invite')


invites = Invite.__table__