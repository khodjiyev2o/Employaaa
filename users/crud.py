from datetime import datetime
from sqlalchemy.orm import Session

from schemas import users as user_schemas
from schemas import companies as company_schemas
from schemas import members as member_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.database import database
from database.models import users,companies,members



class User_Crud():
        def __init__(self,db:Session):
            self.db = db

        async def create_user(self,user: user_schemas.UserSignUp)->user_schemas.User:
            active_user =  await database.fetch_one(users.select().where(users.c.email == user.email))
            if active_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            password = hashing.Hash.bcrypt(user.password)
            db_user = users.insert().values(email=user.email, password=password)
            user_id = await database.execute(db_user)
            return user_schemas.User(**user.dict(),id=user_id)
        
                    
        async def get_user_by_email(self,email: str)->user_schemas.User:
            user = await database.fetch_one(users.select().where(users.c.email == email))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with email {email} not found")
            return user
            
        

        async def get_user_by_id(self,id: int)->user_schemas.User:
            user = await database.fetch_one(users.select().where(users.c.id == id))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            return user

        async def update_user(self,id:int,user:user_schemas.UserUpdate)->user_schemas.User:
            now = datetime.utcnow()
            password = hashing.Hash.bcrypt(user.password)
            active_user = await database.fetch_one(users.select().where(users.c.id == id))
            if active_user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            query = users.update().where(users.c.id == id).values(
            first_name = user.first_name,
            password=password,
            updated_at=now,
            )
            await database.execute(query)
            return await self.get_user_by_id(id=id)

        async def delete_user(self,id:int)->HTTPException:
            user = await database.fetch_one(users.select().where(users.c.id == id))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            query = users.delete().where(users.c.id == id)
            await database.execute(query)
            return HTTPException(status_code=200, detail=f"User with id {id} has been deleted")


        async def get_all_users(self,skip: int = 0, limit: int = 100)->List[user_schemas.User]:
            results = await database.fetch_all(users.select().offset(skip).limit(limit))
            return [user_schemas.User(**result) for result in results]





class Company_Crud():
        def __init__(self,db:Session):
            self.db = db

        async def create_company(self,company: company_schemas.CompanyCreate,user:user_schemas.User)->company_schemas.Company:
            active_company =  await database.fetch_one(companies.select().where(companies.c.name == company.name))
            if active_company:
                raise HTTPException(status_code=400, detail="Company with this name already registered")
            new_company = companies.insert().values(name=company.name,owner_id=user.id)
            company_id = await database.execute(new_company)
            return company_schemas.Company(**company.dict(),id=company_id,owner_id=user.id)


        async def update_company(self,id:int,company: company_schemas.CompanyUpdate)->company_schemas.Company:
            active_company =  await database.fetch_one(companies.select().where(companies.c.id == id))
            if not active_company:
                raise HTTPException(status_code=400, detail="Company with  id {id} does not exist")
            
            query = companies.update().where(
                companies.c.id == id).values(
            visible = company.visible,
            name = company.name,
            description=company.description,
            )
            await database.execute(query)
            return await self.get_company_by_id(id=id)


        async def get_company_by_name(self,name: str)->company_schemas.Company:
            company = await database.fetch_one(companies.select().where(companies.c.name == name))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with name {name} not found")
            return company

        async def get_company_by_id(self,id: int)->company_schemas.Company:
            company = await database.fetch_one(companies.select().where(companies.c.id == id))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with name {id} not found")
            return company


        async def delete_company(self,id:int)->HTTPException:
            company = await database.fetch_one(companies.select().where(companies.c.id == id))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with id {id} not found")
            query = companies.delete().where(companies.c.id == id)
            await database.execute(query)
            return HTTPException(status_code=200, detail=f"Company with id {id} has been deleted")
        
        async def get_all_companies(self,skip: int = 0, limit: int = 100)->List[company_schemas.Company]:
            results = await database.fetch_all(companies.select().where(companies.c.visible == True).offset(skip).limit(limit))
            return [company_schemas.Company(**result) for result in results]



        async def invite_user(self,member: member_schemas.MemberInvite)->member_schemas.Member:
             new_member = members.insert().values(user_id=member.user_id,company_id=member.company_id)
             member_id = await database.execute(new_member)
             return member_schemas.Member(**member.dict(),id=member_id)


        async def s(self,skip: int = 0, limit: int = 100)->List[member_schemas.Member]:
            results = await database.fetch_all(members.select().offset(skip).limit(limit))
            return [member_schemas.Member(**result) for result in results]
       

            
             



