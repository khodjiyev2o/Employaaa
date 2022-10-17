from sqlalchemy.orm import Session
from . import models,schemas

from fastapi import HTTPException,status
from users import hashing

class Crud():
    def __init__(self,db: Session):
        self.db = db

    def get_user_by_id(self,id:int):
        user = self.db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the id {id} is not available")
        return  user

    def get_user_by_email(self,user_email: str ):
        user = self.db.query(models.User).filter(models.User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the email {user_email} is not available")
        return user
    
    def get_users(self, skip: int = 0, limit: int = 100):
        users = self.db.query(models.User).offset(skip).limit(limit).all()
        if not users :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="no users in the database")
        return users 
        
    def create_user(self,user:schemas.UserSignUp):
        password = hashing.Hash.bcrypt(user.password)
        active_user =  self.db.query(models.User).filter(models.User.email == user.email).first()
        if not active_user: 
            db_user = models.User(
                first_name=user.first_name,
                email=user.email,
                password=password,
                phone_number=user.phone_number
                )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with the email {user.email} already exists")
        

    def destroy(self,id:int):
        user = self.db.query(models.User).filter(models.User.id == id)

        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {id} not found")

        user.delete(synchronize_session=False)
        self.db.commit()
        return 'done'


    def update(self,id:int,request:schemas.UserUpdate):
        user = self.db.query(models.User).filter(models.User.id == id)

        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id {id} not found")

        user.update(request)
        self.db.commit()
        return user