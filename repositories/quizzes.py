from asyncio import Task
from datetime import date, datetime
from unittest import result
from venv import create
from sqlalchemy.orm import Session
from repositories.companies import Company_Crud
from sqlalchemy import select, func
from schemas import quizzes as quiz_schemas
from schemas import companies as company_schemas
from schemas import results as result_schemas
from schemas import users as user_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.database import redis_db
from database.models import Question, users,companies,quizzes,questions,results,mean_results,members
from datetime import timedelta
import csv
from fastapi.responses import StreamingResponse



class Quiz_Crud():
        def __init__(self,db:Session):
            self.db = db

        async def create_quiz(self,quiz: quiz_schemas.QuizCreate)->quiz_schemas.Quiz:
            active_quiz =  await self.db.fetch_one(quizzes.select().where(quizzes.c.name == quiz.name))
            if active_quiz:
                raise HTTPException(status_code=400, detail="Quiz already exists")
            
            new_quiz = quizzes.insert().values(
                name=quiz.name,
                description=quiz.description,
                frequency=quiz.frequency,
                company_id = quiz.company_id,
                )
            quiz_id = await self.db.execute(new_quiz)
            return quiz_schemas.Quiz(**quiz.dict(),id=quiz_id)
        
        
        async def get_quiz_by_id(self,id: int)->quiz_schemas.QuizOut:
            quiz = await self.db.fetch_one(quizzes.select().where(quizzes.c.id == id))
            if quiz is None:
                 raise HTTPException(status_code=404, detail=f"Quiz with id {id} not found")
            list_questions = await self.db.fetch_all(questions.select().where(questions.c.quiz_id == quiz["id"]))
            return quiz_schemas.QuizOut(**dict(quiz), questions=[quiz_schemas.Question(**result) for result in list_questions])


        async def get_all_quizzes_for_company_id(self,id: int,skip: int = 0, limit: int = 100)->company_schemas.Company:
            company = await self.db.fetch_one(companies.select().where(companies.c.id == id))
            if company is None:
                 raise HTTPException(status_code=404, detail=f"Company with id {id} not found")
            list_quizzes = await self.db.fetch_all(quizzes.select().where(quizzes.c.company_id == company["id"]).offset(skip).limit(limit))
            return company_schemas.Company(**dict(company), quiz=[quiz_schemas.Quiz(**result) for result in list_quizzes])
    

        async def create_question(self,question:quiz_schemas.QuestionCreate)->quiz_schemas.Question:
            active_question =  await self.db.fetch_one(questions.select().where(questions.c.question == question.question))
            if active_question:
                raise HTTPException(status_code=400, detail="Question already exists")
            new_question = questions.insert().values(
                question=question.question,
                quiz_id=question.quiz_id,
                answer=question.answer,
                options=question.options
                )
            question_id = await self.db.execute(new_question)
            return quiz_schemas.Question(**question.dict(),id=question_id)


        async def delete_quiz(self,id:int)->HTTPException:
            quiz = await self.db.fetch_one(quizzes.select().where(quizzes.c.id == id))
            if quiz is None:
                 raise HTTPException(status_code=404, detail=f"Quiz with id {id} not found")
            query = quizzes.delete().where(quizzes.c.id == id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"Quiz with id {id} has been deleted")
           
           
        async def update_quiz(self,id:int,quiz:quiz_schemas.QuizUpdate)->quiz_schemas.Quiz:
            active_quiz= await self.db.fetch_one(quizzes.select().where(quizzes.c.id == id))
            if active_quiz is None:
                 raise HTTPException(status_code=404, detail=f"Quiz with id {id} not found")
            query = quizzes.update().where(quizzes.c.id == id).values(
            name = quiz.name,
            description=quiz.description,
            frequency=quiz.frequency,
            company_id = quiz.company_id,
            )
            await self.db.execute(query)
            return await self.get_quiz_by_id(id=id)


        async def delete_question(self,id:int)->HTTPException:
            question = await self.db.fetch_one(questions.select().where(questions.c.id == id))
            if question is None:
                 raise HTTPException(status_code=404, detail=f"Question with id {id} not found")
            query = questions.delete().where(questions.c.id == id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"Question with id {id} has been deleted")
        

        async def solve_quiz(self,answer:quiz_schemas.AnswerSheet,user:user_schemas.User)->result_schemas:
            score = 0
            active_quiz = await self.get_quiz_by_id(id=answer.quiz_id)
            quiz_questions  = active_quiz.questions
            user_answers = answer.answers
            ##writing answers to redis
            await self.write_answers_redis(user_id=user.id,answer=answer)

            for user_answers,question in zip(user_answers,quiz_questions):
                if user_answers.question_id == question.id and user_answers.answer == question.answer:
                    score+=1
            
            ##calculate mean result
            all_questions_by_quiz =  await self.db.fetch_all(questions.select().where(questions.c.quiz_id == answer.quiz_id )) 
            questions_length = len(all_questions_by_quiz)
            mean_result = await self.calculate_mean_result(user=user,current_quiz=result_schemas.Mean_Result(user_id=user.id,num_of_qs=questions_length,num_of_ans=score,mean_result=0))
            
            db_result = results.insert().values(
                 company_id=active_quiz.company_id,
                 quiz_id=answer.quiz_id,
                 user_id=user.id,
                 result=score,
                 mean_result=mean_result,
                 )
            result_id = await self.db.execute(db_result)
            return  result_schemas.Result(id=result_id,user_id=user.id,company_id=active_quiz.company_id,result=score,quiz_id=active_quiz.id,mean_result=mean_result,date_solved=datetime.utcnow())
             
      
        async def write_answers_redis(self,user_id:int,answer:quiz_schemas.AnswerSheet)->str:
            user_answers = answer.answers
            res = {}
            for i in user_answers:
                    key_j = '{}'.format(i.question_id)  
                    res[key_j] = i.answer
            await redis_db.hset(f"{user_id}", mapping=res)
            await redis_db.expire(f'{user_id}',timedelta(hours=48))
            await redis_db.close()
           

        async def get_all_quizzes_with_time(self,user_id,skip: int = 0, limit: int = 100)->quiz_schemas.QuizWithTime:
             quizzes = await self.db.fetch_all(results.select().offset(skip).limit(limit))
             list_of_quiz_ids = [result.quiz_id for result in quizzes]            
             unique_ids = []
             _ = [unique_ids.append(id) for id in list_of_quiz_ids if id not in unique_ids]
             for quiz_id in unique_ids:
                quizzes = await self.db.fetch_all(results.select().where(results.c.quiz_id == quiz_id,results.c.user_id==user_id))
                return [quiz_schemas.QuizWithTime(**result,last_time_solved=result.date_solved) for result in quizzes]

        async def calculate_mean_result(self,current_quiz:result_schemas.Mean_Result,user:user_schemas.User)->int:
            mean_result_model = await self.db.fetch_one(mean_results.select().where(mean_results.c.user_id == user.id))
            if not mean_result_model:
                new_mean_score = current_quiz.num_of_ans/current_quiz.num_of_qs
                new_mean_score_percentage = int(new_mean_score*100)
                query_1 = mean_results.insert().values(
                user_id=user.id,
                num_of_qs=current_quiz.num_of_qs,
                num_of_ans=current_quiz.num_of_ans,
                mean_result = new_mean_score_percentage,
                )
                id = await self.db.execute(query_1)
                query = users.update().where(users.c.id == user.id).values(
                mean_result=new_mean_score_percentage
                )
                await self.db.execute(query)
                return result_schemas.Mean_ResultCreate(**current_quiz.dict(),id=id)

            new_num_of_qs = mean_result_model.num_of_qs+current_quiz.num_of_qs
            new_num_of_ans = mean_result_model.num_of_ans+current_quiz.num_of_ans
            new_mean_score_percentage = int((new_num_of_ans/new_num_of_qs)*100)
            query_1 = mean_results.update().where(mean_results.c.id == mean_result_model.id).values(
            num_of_qs=new_num_of_qs,
            num_of_ans=new_num_of_ans,
            mean_result = new_mean_score_percentage,
            )
            id = await self.db.execute(query_1)
            
            query = users.update().where(users.c.id == user.id).values(
            mean_result=new_mean_score_percentage
            )
            await self.db.execute(query)
            mean_result_model.meanresult == new_mean_score_percentage
            return  new_mean_score_percentage


        async def get_result_of_user(self,user_id)->StreamingResponse:
            data = await redis_db.hgetall(f'{user_id}')
            column_names = ["Question_id","Answer"]
            user_data = []
            data = dict(data)
            for i in data:
                arr = [i,data[i]]    
                user_data.append(arr)
            csv = await self.write_csv(user_id=user_id,user_data=user_data,column_names=column_names,file_name=user_id)
            return csv 


        async def get_all_results_of_users(self,company)->StreamingResponse:
             list_of_members = await self.db.fetch_all(members.select().where(members.c.company_id == company.id))
             list_of_ids = [dict(**member)['user_id']  for  member in list_of_members]  
             column_names = ["User_Id","Question_id","Answer"]    
             user_data = []
             for id in list_of_ids:
                data = await redis_db.hgetall(f'{id}')
                data = dict(data)
                if data:
                    for i in data:
                        arr = [id,i,data[i]]    
                        user_data.append(arr)
             
             csv = await self.write_csv(user_id=id,user_data=user_data,column_names=column_names,file_name="all_users_results")
             return csv


        async def write_csv(self,user_id:int,user_data:list,column_names:list,file_name:str)->StreamingResponse:





            with open(f'{file_name}.csv','w',encoding="UTF-8",newline="") as f :
                writer = csv.writer(f)
                writer.writerow(column_names)
                writer.writerows(user_data)
            csv_file = open(f"{file_name}.csv", mode="rb")
            export_media_type = 'text/csv'
            export_headers = {
                "Content-Disposition": "attachment; filename={file_name}.csv".format(file_name=file_name)
            }
            return StreamingResponse(csv_file, headers=export_headers, media_type=export_media_type)


