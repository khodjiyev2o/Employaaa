from sqlalchemy.orm import Session
from . import models,schemas

def get_user_by_id(db:Session,user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session,user_email: str ):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db:Session,user:schemas.UserSignUp):
    password = user.password 
    db_user = models.User(
        first_name=user.first_name,
        email=user.email,
        password=password,
        phone_number=user.phone_number
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


