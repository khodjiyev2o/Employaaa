from datetime import datetime
from sqlalchemy.orm import Session

from schemas import users as user_schemas
from schemas import companies as company_schemas
from schemas import members as member_schemas
from schemas import invites as invite_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.database import database
from database.models import users,companies,members,invites



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
            fetched_users = await database.fetch_all(users.select().offset(skip).limit(limit))
            new_list=[]
            for user in fetched_users:
                user = dict(user)
                list_invites = await database.fetch_all(invites.select().where(invites.c.user_id == user["id"]))
                user.update({"invite": [dict(result) for result in list_invites]})
                new_list.append(user)
            return [user_schemas.User(**result) for result in new_list]

        async def accept_invite(self,invite:invite_schemas.InviteCreate)->member_schemas.MemberOut:
            active_member = await database.fetch_one(members.select().where(members.c.company_id == invite.company_id,members.c.user_id == invite.user_id))
            if active_member:
                raise HTTPException(status_code=403,detail=f"User with id {invite.user_id} is already member in company with id {invite.company_id}")
            member = members.insert().values(company_id=invite.company_id, user_id=invite.user_id)
            member_id = await database.execute(member)
            self.decline_invite(invite=invite)
            return member_schemas.MemberOut(**invite.dict(),id=member_id)
        
        async def decline_invite(self,invite:invite_schemas.InviteCreate)->HTTPException:
            active_invite = await database.fetch_one(invites.select().where(invites.c.user_id == invite.user_id,invites.c.company_id == invite.company_id))
            if not active_invite:
                raise HTTPException(status_code=404,detail=f"Invite to the company with id{invite.company_id} not found")
            query = invites.delete().where(invites.c.user_id == invite.user_id,invites.c.company_id == invite.company_id)
            await database.execute(query)
            return HTTPException(status_code=200,detail=f"Invite to the company with id {invite.company_id} was succesfully declined")
        
        async def apply_to_company(self,application:invite_schemas.InviteCreate)->invite_schemas.Invite:
            active_application = await database.fetch_one(invites.select().where(invites.c.user_id == application.user_id,invites.c.company_id == application.company_id))
            member = await database.fetch_one(members.select().where(members.c.user_id == application.user_id,members.c.company_id == application.company_id))
            if  active_application or member:
                raise HTTPException(status_code=404,detail=f"You have already applied to the  company with id {application.company_id}")
            query = invites.insert().values(user_id=application.user_id,company_id=application.company_id)
            new_application_id = await database.execute(query)
            return invite_schemas.Invite(**application.dict(),id=new_application_id)




