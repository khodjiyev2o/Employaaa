from sqlalchemy.orm import Session
from . import models,schemas

from fastapi import HTTPException,status
from users import hashing


def get_user_by_id(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

def get_user_by_email(db:Session,user_email: str ):
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {user_email} is not available")
    return user
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no users in the database")
    return users 
    
def create_user(user:schemas.UserSignUp,db:Session):
    password = hashing.Hash.bcrypt(user.password)
    active_user =  db.query(models.User).filter(models.User.email == user.email).first()
    if not active_user: 
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
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with the email {user.email} already exists")
    

def destroy(id:int,db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id:int,request:schemas.UserUpdate, db:Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.update(request)
    db.commit()
    return user