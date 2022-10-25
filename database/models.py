from email.mime import application
from sqlalchemy import Column, DateTime,Integer, String,ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


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
    quiz = relationship("Quizz",back_populates='company')
companies=Company.__table__


class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    is_admin = Column(Boolean, server_default='FALSE')

    company_id = Column(Integer, ForeignKey("companies.id"))


    company = relationship("Company",back_populates='members')


members=Member.__table__



class Invite(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    company_id = Column(Integer, ForeignKey("companies.id",ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))


    company = relationship("Company",back_populates='application')
    user = relationship("User",back_populates='invite')


invites = Invite.__table__




class Quizz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    name =  description = Column(String,unique=True)
    description =  Column(String)
    frequency = Column(Integer)
    questions = relationship("Question",back_populates='quiz')
    company_id = Column(Integer, ForeignKey("companies.id",ondelete="CASCADE"))


    company = relationship("Company",back_populates='quiz')
quizzes = Quizz.__table__

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    question = Column(String)
    quiz_id = Column(Integer, ForeignKey("quizzes.id",ondelete="CASCADE"))
    quiz = relationship("Quizz",back_populates='questions')
    

    answer = Column(String)
    options = Column(ARRAY(String),nullable=False,)
  
questions = Question.__table__

    