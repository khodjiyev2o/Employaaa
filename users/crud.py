from datetime import datetime
from sqlalchemy.orm import Session
from . import models,schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from .database import database
from .models import users
from . import schemas

class Crud():
        def __init__(self,db:Session):
            self.db = db

        async def create_user(self,user: schemas.UserSignUp)->schemas.User:
            active_user =  await database.fetch_one(users.select().where(users.c.email == user.email))
            if active_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            password = hashing.Hash.bcrypt(user.password)
            db_user = users.insert().values(email=user.email, password=password)
            user_id = await database.execute(db_user)
            return schemas.User(**user.dict(),id=user_id)
        
                    
        async def get_user_by_email(self,email: str)->schemas.User:
            return await database.fetch_one(users.select().where(users.c.email == email))
        

        async def get_user_by_id(self,id: int)->schemas.User:
            user = await database.fetch_one(users.select().where(users.c.id == id))
            if user is None:
                 raise HTTPException(status_code=404, detail="User not found")
            return user

        async def update_user(self,id:int,user:schemas.UserUpdate)->schemas.User:
            now = datetime.utcnow()
            query = users.update().where(users.c.id == id).values(
            first_name = user.first_name,
            phone_number=user.phone_number,
            updated_at=now,
            )
            await database.execute(query)

            return schemas.User(**user.dict(),id=id)

        async def delete_user(self,id:int)->str:
            query = users.delete().where(users.c.id == id)
            await database.execute(query)
            return {f"User with id {id} is successfully deleted"}


        async def get_all_users(self,skip: int = 0, limit: int = 100)->List[schemas.User]:
            results = await database.fetch_all(users.select().offset(skip).limit(limit))
            return [dict(result) for result in results]