from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import quizzes as quiz_schemas
from schemas import companies as company_schemas
from database import database
from repositories.companies import Company_Crud  
from repositories.users import User_Crud 
from repositories.quizzes import Quiz_Crud
from authentication.auth import AuthHandler
from database.models import members
from database.database import database as db
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



@router.get("/all-quizzes/", response_model=company_schemas.Company)
async def get_all_quizzes_for_company_id(id:int,skip: int = 0, limit: int = 100)->company_schemas.Company:
    crud = Quiz_Crud(get_db)
    return await crud.get_all_quizzes_for_company_id(id=id,skip=skip, limit=limit)


@router.post("/create/")
async def create_quiz(quiz: quiz_schemas.QuizCreate)->quiz_schemas.Quiz:
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


@router.delete("/delete/{id}")
async def delete_quiz(id: int,quiz:quiz_schemas.Quiz,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Quiz_Crud(get_db)
    user_crud = User_Crud(get_db)
    current_user = await user_crud.get_user_by_email(email=current_user_email)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz.company_id)
    if current_user.id != company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's account!")
    return await crud.delete_quiz(id=id)



@router.patch("/update/{id}",response_model=quiz_schemas.Quiz)
async def update_user(id: int,quiz:quiz_schemas.QuizUpdate,current_user_email=Depends(auth_handler.get_current_user))->quiz_schemas.Quiz:
    crud = User_Crud(get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    company = await Company_Crud(get_db).get_company_by_id(id=quiz.company_id)
    member = await db.fetch_one(members.select().where(members.c.user_id == current_user.id,members.c.company_id == company.id))
    if current_user.id != company.owner_id:
        try:
            if current_user.id == member.user_id :
                return await Quiz_Crud(get_db).update_quiz(quiz=quiz,id=id)
        except AttributeError:
                raise  HTTPException(status_code=403, detail="User is not authorized to update another user's company!")
    return await Quiz_Crud(get_db).update_quiz(quiz=quiz,id=id)
