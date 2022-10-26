from datetime import datetime
from sqlalchemy.orm import Session

from schemas import users as user_schemas
from schemas import companies as company_schemas
from schemas import members as member_schemas
from schemas import invites as invite_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.models import Invite, users,companies,members,invites




class Company_Crud():
        def __init__(self,db:Session):
            self.db = db

        async def create_company(self,company: company_schemas.CompanyCreate,user:user_schemas.User)->company_schemas.Company:
            active_company =  await self.db.fetch_one(companies.select().where(companies.c.name == company.name))
            if active_company:
                raise HTTPException(status_code=400, detail="Company with this name already registered")
            new_company = companies.insert().values(name=company.name,owner_id=user.id)
            company_id = await self.db.execute(new_company)
            return company_schemas.Company(**company.dict(),id=company_id,owner_id=user.id)


        async def update_company(self,id:int,company: company_schemas.CompanyUpdate)->company_schemas.Company:
            active_company =  await self.db.fetch_one(companies.select().where(companies.c.id == id))
            if not active_company:
                raise HTTPException(status_code=400, detail="Company with  id {id} does not exist")
            
            query = companies.update().where(
                companies.c.id == id).values(
            visible = company.visible,
            name = company.name,
            description=company.description,
            )
            await self.db.execute(query)
            return await self.get_company_by_id(id=id)


        async def get_company_by_name(self,name: str)->company_schemas.Company:
            company = await self.db.fetch_one(companies.select().where(companies.c.name == name))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with name {name} not found")
            list_members = await self.db.fetch_all(members.select().where(members.c.company_id == company["id"]))
            list_applications = await self.db.fetch_all(invites.select().where(invites.c.company_id == company["id"]))
            return company_schemas.Company(**dict(company), members=[member_schemas.Member(**result) for result in list_members], applications=[invite_schemas.Invite(**result) for result in list_applications])

        async def get_company_by_id(self,id: int)->company_schemas.Company:
            company = await self.db.fetch_one(companies.select().where(companies.c.id == id))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with name {id} not found")
            return company_schemas.Company(**dict(company))


        async def delete_company(self,id:int)->HTTPException:
            company = await self.db.fetch_one(companies.select().where(companies.c.id == id))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with id {id} not found")
            query = companies.delete().where(companies.c.id == id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"Company with id {id} has been deleted")
        
        async def get_all_companies(self,skip: int = 0, limit: int = 100)->List[company_schemas.Company]:
            results = await self.db.fetch_all(companies.select().where(companies.c.visible == True).offset(skip).limit(limit))
            return [company_schemas.Company(**result) for result in results]



        async def invite_user(self,invite: invite_schemas.InviteCreate)->invite_schemas.Invite:
             active_invite =  await self.db.fetch_one(invites.select().where(invites.c.user_id == invite.user_id,invites.c.company_id == invite.company_id))
             if active_invite:
                raise HTTPException(status_code=400, detail=f"User with the id{invite.user_id} has already  been invited to the company with id {invite.company_id}")
             new_invite = invites.insert().values(user_id=invite.user_id,company_id=invite.company_id)
             invite_id = await self.db.execute(new_invite)
             return invite_schemas.Invite(**invite.dict(),id=invite_id)


        async def get_members(self,skip: int = 0, limit: int = 100)->List[member_schemas.Member]:
            results = await self.db.fetch_all(members.select().offset(skip).limit(limit))
            return [member_schemas.Member(**result) for result in results]
       


        async def accept_user(self,application:invite_schemas.InviteCreate)->member_schemas.MemberOut:
            member = await self.db.fetch_one(members.select().where(members.c.company_id == application.company_id,members.c.user_id == application.user_id))
            if member:
                 raise HTTPException(status_code=404, detail=f"Member with User_ID {member.user_id} already in the company ")
            query = members.insert().values(user_id=application.user_id,company_id=application.company_id)
            member_id = await self.db.execute(query)
            delete_application = invites.delete().where(invites.c.user_id == application.user_id,invites.c.company_id == application.company_id)
            await self.db.execute(delete_application)
            return member_schemas.MemberOut(**application.dict(),id=member_id)



        async def delete_member(self,member:member_schemas.MemberDelete)->HTTPException:
            member = await self.db.fetch_one(members.select().where(members.c.company_id == member.company_id,members.c.user_id == member.user_id))
            if member is None:
                 raise HTTPException(status_code=404, detail=f"Member with User_ID {member.user_id} not found")
            query = members.delete().where(members.c.id == member.id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"Member with User_ID {member.user_id} has been deleted")
        
        async def get_member(self,member:member_schemas.MemberUpdate)->member_schemas.Member:
            active_member = await self.db.fetch_one(members.select().where(members.c.user_id == member.user_id,members.c.company_id == member.company_id))
            if active_member is None:
                 raise HTTPException(status_code=404, detail=f"Member with User id {member.user_id} not found")
            return member_schemas.Member(**dict(member))

        ##make admin
        async def update_admin(self,member:member_schemas.MemberUpdate)->member_schemas.Member:
            active_member =  await self.db.fetch_one(members.select().where(members.c.company_id == member.company_id,members.c.user_id == member.user_id))
            if not active_member:
                raise HTTPException(status_code=400, detail=f"Member with User id {id} does not exist")
            query = members.update().where(
                members.c.company_id == member.company_id,members.c.user_id == member.user_id).values(
            is_admin=member.is_admin
            )
            await self.db.execute(query)
            return await self.get_member(member=member)
             