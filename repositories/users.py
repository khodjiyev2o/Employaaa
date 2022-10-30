from datetime import datetime
from sqlalchemy.orm import Session

from schemas import quizzes, users as user_schemas
from schemas import companies as company_schemas
from schemas import members as member_schemas
from schemas import invites as invite_schemas
from schemas import results as result_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.models import Mean_Result, users,companies,members,invites,results,mean_results,questions
from repositories.companies import Company_Crud  
from repositories.quizzes import Quiz_Crud

class User_Crud():
        def __init__(self,db:Session):
            self.db = db
#USER-CRUD
        async def create_user(self,user: user_schemas.UserSignUp)->user_schemas.User:
            active_user =  await self.db.fetch_one(users.select().where(users.c.email == user.email))
            if active_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            password = hashing.Hash.bcrypt(user.password)
            db_user = users.insert().values(email=user.email, password=password)
            user_id = await self.db.execute(db_user)
            return user_schemas.User(**user.dict(),id=user_id)
        
                    
        async def get_user_by_email(self,email: str)->user_schemas.User:
            user = await self.db.fetch_one(users.select().where(users.c.email == email))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with email {email} not found")
            return user_schemas.User(**dict(user))
            
        
        async def get_user_by_id(self,id: int)->user_schemas.User:
            user = await self.db.fetch_one(users.select().where(users.c.id == id))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            list_result = await self.db.fetch_all(results.select().where(results.c.user_id == user.id))
            return user_schemas.User(**dict(user),result=[result_schemas.UserResult(**result) for result in list_result])


        async def update_user(self,id:int,user:user_schemas.UserUpdate)->user_schemas.User:
            now = datetime.utcnow()
            password = hashing.Hash.bcrypt(user.password)
            active_user = await self.db.fetch_one(users.select().where(users.c.id == id))
            if active_user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            query = users.update().where(users.c.id == id).values(
            first_name = user.first_name,
            password=password,
            updated_at=now,
            )
            await self.db.execute(query)
            return await self.get_user_by_id(id=id)


        async def delete_user(self,id:int)->HTTPException:
            user = await self.db.fetch_one(users.select().where(users.c.id == id))
            if user is None:
                 raise HTTPException(status_code=404, detail=f"User with id {id} not found")
            query = users.delete().where(users.c.id == id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"User with id {id} has been deleted")


        async def get_all_users(self,skip: int = 0, limit: int = 100)->List[user_schemas.User]:
            fetched_users = await self.db.fetch_all(users.select().offset(skip).limit(limit))
            new_list=[]
            for user in fetched_users:
                user = dict(user)
                list_invites = await self.db.fetch_all(invites.select().where(invites.c.user_id == user["id"]))
                user.update({"invite": [dict(result) for result in list_invites]})
                new_list.append(user)
            return [user_schemas.User(**result) for result in new_list]

#COMPANY-INVITES
        async def accept_invite(self,invite:invite_schemas.InviteCreate)->member_schemas.MemberOut:
            active_member = await self.db.fetch_one(members.select().where(members.c.company_id == invite.company_id,members.c.user_id == invite.user_id))
            if active_member:
                raise HTTPException(status_code=403,detail=f"User with id {invite.user_id} is already member in company with id {invite.company_id}")
            member = members.insert().values(company_id=invite.company_id, user_id=invite.user_id)
            member_id = await self.db.execute(member)
            self.decline_invite(invite=invite)
            return member_schemas.MemberOut(**invite.dict(),id=member_id)


        async def decline_invite(self,invite:invite_schemas.InviteCreate)->HTTPException:
            active_invite = await self.db.fetch_one(invites.select().where(invites.c.user_id == invite.user_id,invites.c.company_id == invite.company_id))
            if not active_invite:
                raise HTTPException(status_code=404,detail=f"Invite to the company with id{invite.company_id} not found")
            query = invites.delete().where(invites.c.user_id == invite.user_id,invites.c.company_id == invite.company_id)
            await self.db.execute(query)
            return HTTPException(status_code=200,detail=f"Invite to the company with id {invite.company_id} was succesfully declined")


        async def apply_to_company(self,application:invite_schemas.InviteCreate)->invite_schemas.Invite:
            active_application = await self.db.fetch_one(invites.select().where(invites.c.user_id == application.user_id,invites.c.company_id == application.company_id))
            member = await self.db.fetch_one(members.select().where(members.c.user_id == application.user_id,members.c.company_id == application.company_id))
            if  active_application or member:
                raise HTTPException(status_code=404,detail=f"You have already applied to the  company with id {application.company_id}")
            query = invites.insert().values(user_id=application.user_id,company_id=application.company_id)
            new_application_id = await self.db.execute(query)
            return invite_schemas.Invite(**application.dict(),id=new_application_id)

#USER-ANALYTICS

        async def get_all_users_mean_result(self,skip: int = 0, limit: int = 100)->List[result_schemas.AllUserMeanResult]:
                fetched_users = await self.db.fetch_all(mean_results.select().offset(skip).limit(limit))
                return [result_schemas.AllUserMeanResult(**result) for result in fetched_users]

                   
        async def get_user_mean_result_from_all_quizzes(self,user_id:int)->list:
            list_of_quizzes_with_mean_results = []
            list_of_results = await self.db.fetch_all(results.select().where(results.c.user_id == user_id))
            list_of_quiz_ids = [result.quiz_id for result in list_of_results]            
            unique_ids = []
            _ = [unique_ids.append(id) for id in list_of_quiz_ids if id not in unique_ids]
            for quiz_id in unique_ids:
                quizzes = await self.db.fetch_all(results.select().where(results.c.quiz_id == quiz_id,results.c.user_id == user_id))
                times_solved = len(quizzes)
                sum_of_quiz_results = sum([result.result for result in quizzes])
                all_questions_by_quiz =  await self.db.fetch_all(questions.select().where(questions.c.quiz_id == quiz_id )) 
                questions_length = len(all_questions_by_quiz) 
                mean_result_by_quiz = int((sum_of_quiz_results/(questions_length*times_solved))*100)
                last_time_solved = [result.date_solved for result in quizzes]
                mean_result_by_quiz = result_schemas.UserMeanResultQuiz(user_id=user_id,quiz_id=quiz_id,mean_result=mean_result_by_quiz,last_time_solved=last_time_solved[-1])
                list_of_quizzes_with_mean_results.append(mean_result_by_quiz)
            return list_of_quizzes_with_mean_results

        
        async def get_user_mean_result_from_each_quiz(self,user_id:int)->List[result_schemas.UserMeanResultAllQuiz]:
            list_of_quizzes = []
            list_of_results = await self.db.fetch_all(results.select().where(results.c.user_id == user_id))
            list_of_quiz_ids = [result.quiz_id for result in list_of_results]    
            unique_ids = []
            _ = [unique_ids.append(id) for id in list_of_quiz_ids if id not in unique_ids]
            for quiz_id in unique_ids:
                quizzes = await self.db.fetch_all(results.select().where(results.c.quiz_id == quiz_id,results.c.user_id == user_id))
                times_solved = len(quizzes)
                total_mean_result = sum([result.mean_result for result in quizzes])
                tota_mean_result_by_quiz = int((total_mean_result/times_solved))
                last_time_solved = [result.date_solved for result in quizzes]
                list_of_quizzes.append(result_schemas.UserMeanResultAllQuiz(quiz_id=quiz_id,mean_result=tota_mean_result_by_quiz,last_time_solved=last_time_solved[-1]))
            return list_of_quizzes

#Check if the  user is admin or not 

        async def checking_for_admin(self,company_id,current_user_email):
                company_crud = Company_Crud(self.db)
                company = await company_crud.get_company_by_id(id=company_id)
                current_user = await self.get_user_by_email(email=current_user_email)
                member = await self.db.fetch_one(members.select().where(members.c.user_id == current_user.id,members.c.company_id == company.id))
                if current_user.id != company.owner_id:
                    try:
                        if current_user.id == member.user_id and member.is_admin == True :
                            return True
                        else: 
                            raise HTTPException(status_code=403, detail="User is not authorized to get  all  users's results!")
                    except AttributeError:
                            raise  HTTPException(status_code=403, detail="User is not authorized to get  another user's results!")
                return True