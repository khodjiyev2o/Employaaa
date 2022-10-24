from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import quizzes as quiz_schemas
from database import database
from repositories.companies import Company_Crud  
from repositories.users import User_Crud 
from repositories.quizzes import Quiz_Crud
from authentication.auth import AuthHandler


auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db


# @router.get("/get-all/", response_model=List[schemas.Company])
# async def get_all_companies(skip: int = 0, limit: int = 100,current_user_email=Depends(auth_handler.get_current_user))->List[schemas.Company]:
#     crud = Company_Crud(get_db)
#     return await crud.get_all_companies(skip=skip, limit=limit)


@router.post("/create/")
async def create_quiz(quiz: quiz_schemas.Quiz)->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    return await quiz_crud.create_quiz(quiz=quiz)

@router.post("/create/question")
async def create_question(question: quiz_schemas.QuestionCreate)->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    return await quiz_crud.create_question(question=question)

@router.get("/get/{id}")
async def get_quiz_by_id(id:int)->quiz_schemas.Quiz:
    quiz_crud = Quiz_Crud(get_db)
    return await quiz_crud.get_quiz_by_id(id=id)
