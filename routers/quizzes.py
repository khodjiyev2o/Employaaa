from curses.ascii import HT
from signal import raise_signal
from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import quizzes as quiz_schemas
from schemas import companies as company_schemas
from schemas import results as result_schemas
from repositories.companies import Company_Crud  
from repositories.users import User_Crud 
from repositories.quizzes import Quiz_Crud
from authentication.auth import AuthHandler
from database.models import members,questions
from database.database import redis_db
from database.database import database as get_db
from fastapi.responses import StreamingResponse


auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Not found"}},
)








@router.get("/all-quizzes/", response_model=company_schemas.Company)
async def get_all_quizzes_for_company_id(id:int,company_id:int,skip: int = 0, limit: int = 100,current_user_email=Depends(auth_handler.get_current_user))->company_schemas.Company:
    crud = Quiz_Crud(get_db)    
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    if admin is True:
        company = await crud.get_all_quizzes_for_company_id(id=id,skip=skip, limit=limit)
        return company


@router.post("/create/",response_model=quiz_schemas.QuizCreate)
async def create_quiz(quiz: quiz_schemas.QuizCreate,company_id:int,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    if admin is True:
        quiz = await quiz_crud.create_quiz(quiz=quiz)
        return quiz

@router.post("/create/question",response_model=quiz_schemas.Question)
async def create_question(question: quiz_schemas.QuestionCreate,company_id:int,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    if admin is True:
        question = await quiz_crud.create_question(question=question)
        return question

@router.get("/get/{id}",response_model=quiz_schemas.QuizOut)
async def get_quiz_by_id(id:int)->quiz_schemas.QuizOut:
    quiz_crud = Quiz_Crud(get_db)
    quiz = await quiz_crud.get_quiz_by_id(id=id)
    return quiz


@router.delete("/delete/quiz/{id}",status_code=200)
async def delete_quiz(id: int,company_id:int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Quiz_Crud(get_db)
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    if admin is True:
        return await crud.delete_quiz(id=id)


@router.delete("/delete/question/{id}",status_code=200)
async def delete_question(id: int,company_id:int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Quiz_Crud(get_db)
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    if admin is True:
        return await crud.delete_question(id=id)


@router.patch("/update/{id}",response_model=quiz_schemas.Quiz)
async def update_quiz(id: int,quiz:quiz_schemas.QuizUpdate,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=quiz.company_id,current_user_email=current_user_email)
    if admin is True:
        return await Quiz_Crud(get_db).update_quiz(quiz=quiz,id=id)





@router.post("/solve/quiz")
async def solve_quiz(answer: quiz_schemas.AnswerSheet,current_user_email=Depends(auth_handler.get_current_user))->result_schemas.Result:
    crud = User_Crud(get_db)
    user = await crud.get_user_by_email(email=current_user_email)
    results = await Quiz_Crud(db=get_db).solve_quiz(answer=answer,user=user)
    return results


@router.get("/get_csv_for_user")
async def get_result_of_user(user_id:int,company_id:int,current_user_email=Depends(auth_handler.get_current_user))->StreamingResponse: 
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    current_user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    if admin is True or user_id==current_user.id:
        csv = await Quiz_Crud(db=get_db).get_result_of_user(user_id=user_id)
        return csv 




@router.get("/get_all_results_of_user")
async def get_all_results_of_users(company_id:int,current_user_email=Depends(auth_handler.get_current_user))->StreamingResponse:
    admin = await User_Crud(db=get_db).checking_for_admin(company_id=company_id,current_user_email=current_user_email)
    company = await Company_Crud(db=get_db).get_company_by_id(id=company_id)
    if admin is True:
        csv = await Quiz_Crud(db=get_db).get_all_results_of_users(company=company)
        return csv