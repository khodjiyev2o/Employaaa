from asyncio import Task
from datetime import datetime
from venv import create
from sqlalchemy.orm import Session
from repositories.companies import Company_Crud

from schemas import quizzes as quiz_schemas
from schemas import companies as company_schemas
from schemas import results as result_schemas
from schemas import users as user_schemas
from typing import List
from fastapi import HTTPException,status
from users import hashing
from database.database import database
from database.models import users,companies,members,invites,quizzes,questions,results
from schemas.quizzes import AnswerRedis


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
        
                    ##insert questions and options also

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



            ##delete quiz
        async def delete_quiz(self,id:int)->HTTPException:
            quiz = await self.db.fetch_one(quizzes.select().where(quizzes.c.id == id))
            if quiz is None:
                 raise HTTPException(status_code=404, detail=f"Quiz with id {id} not found")
            query = quizzes.delete().where(quizzes.c.id == id)
            await self.db.execute(query)
            return HTTPException(status_code=200, detail=f"Quiz with id {id} has been deleted")
           
           
            ##update quiz

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
            for user_answers,question in zip(user_answers,quiz_questions):
                answer_redis =  AnswerRedis(question_id=user_answers.question_id,
                                            answer = user_answers.answer
                                                )
                print(answer_redis)
                await self.create(answer_redis=answer_redis)
                if user_answers.question_id == question.id and user_answers.answer == question.answer:
                    score+=1
            db_result = results.insert().values(
                 company_id=active_quiz.company_id,
                 quiz_id=answer.quiz_id,
                 user_id=user.id,
                 result=score
                 )
            result_id = await self.db.execute(db_result)
            return  result_schemas.Result(id=result_id,
                                        user_id=user.id,
                                        company_id=active_quiz.company_id,
                                        result=score,
                                        quiz_id=active_quiz.id
                                        )
             
        async def create(answer_redis: AnswerRedis):
            return answer_redis.save()
