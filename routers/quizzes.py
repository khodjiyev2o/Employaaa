from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import quizzes as quiz_schemas
from schemas import companies as company_schemas
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



@router.get("/all-quizzes/", response_model=company_schemas.Company)
async def get_all_quizzes_for_company_id(id:int,skip: int = 0, limit: int = 100)->company_schemas.Company:
    crud = Quiz_Crud(get_db)
    return await crud.get_all_quizzes_for_company_id(id=id,skip=skip, limit=limit)



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



# @router.delete("/delete/{id}")
# async def delete_quiz(id: int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
#     quiz_crud = Quiz_Crud(get_db)
#     active_quiz = await quiz_crud.get_company_by_id(id=id)
#     if not active_quiz:
#         raise HTTPException(status_code=404, detail=f"Quiz with id {id} not found")
#     current_user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
#     if current_user.id != active_quiz.owner_id :
#         raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's company!")
#     return await company_crud.delete_company(id=id)