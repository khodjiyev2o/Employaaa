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

from database.database import database as get_db

auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Not found"}},
)








@router.get("/all-quizzes/", response_model=company_schemas.Company)
async def get_all_quizzes_for_company_id(id:int,skip: int = 0, limit: int = 100,current_user_email=Depends(auth_handler.get_current_user))->company_schemas.Company:
    crud = Quiz_Crud(get_db)    
    user_crud = User_Crud(get_db)
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    company = await Company_Crud(get_db).get_company_by_id(id=id)
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's account!")
    company = await crud.get_all_quizzes_for_company_id(id=id,skip=skip, limit=limit)
    return company


@router.post("/create/",response_model=quiz_schemas.QuizCreate)
async def create_quiz(quiz: quiz_schemas.QuizCreate,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    user_crud = User_Crud(get_db)
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz.company_id)
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's account!")
    quiz = await quiz_crud.create_quiz(quiz=quiz)
    return quiz

@router.post("/create/question",response_model=quiz_schemas.Question)
async def create_question(question: quiz_schemas.QuestionCreate,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    user_crud = User_Crud(get_db)
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    quiz = await quiz_crud.get_quiz_by_id(id=question.quiz_id)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz['company_id'])
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's account!")
    question = await quiz_crud.create_question(question=question)
    return question

@router.get("/get/{id}",response_model=quiz_schemas.QuizOut)
async def get_quiz_by_id(id:int)->quiz_schemas.QuizOut:
    quiz_crud = Quiz_Crud(get_db)
    quiz = await quiz_crud.get_quiz_by_id(id=id)
    return quiz


@router.delete("/delete/quiz/{id}",status_code=200)
async def delete_quiz(id: int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Quiz_Crud(get_db)
    user_crud = User_Crud(get_db)
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    quiz = await crud.get_quiz_by_id(id=id)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz['company_id'])
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's company quizzes!")
    return await crud.delete_quiz(id=id)

@router.delete("/delete/question/{id}",status_code=200)
async def delete_question(id: int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Quiz_Crud(get_db)
    user_crud = User_Crud(get_db)   
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    question = await get_db.fetch_one(questions.select().where(questions.c.id == id))
    if not question:
        raise HTTPException(status_code=404, detail=f"Question with id {id} does not exist")
    quiz =  await crud.get_quiz_by_id(id=question.quiz_id)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz['company_id'])
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's company questions!")
    return await crud.delete_question(id=id)

@router.patch("/update/{id}",response_model=quiz_schemas.Quiz)
async def update_quiz(id: int,quiz:quiz_schemas.QuizUpdate,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    crud = User_Crud(get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz.company_id)
    member = await get_db.fetch_one(members.select().where(members.c.user_id == current_user.id,members.c.company_id == company.id))
    if current_user.id != company.owner_id:
        try:
            if current_user.id == member.user_id :
                return await Quiz_Crud(get_db).update_quiz(quiz=quiz,id=id)
        except AttributeError:
                raise  HTTPException(status_code=403, detail="User is not authorized to update another user's company!")
    return await Quiz_Crud(get_db).update_quiz(quiz=quiz,id=id)





@router.post("/solve/quiz")
async def create_question(answer: quiz_schemas.AnswerSheet,current_user_email=Depends(auth_handler.get_current_user))->result_schemas.Result:
    crud = User_Crud(get_db)
    user = await crud.get_user_by_email(email=current_user_email)
    results = await Quiz_Crud(db=get_db).solve_quiz(answer=answer,user=user)
    return results