from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import companies as schemas
from database import database
from users.crud import Company_Crud  
from users.crud import User_Crud 
from authentication.auth import AuthHandler


auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db




@router.post("/create/",response_model=schemas.Company)
async def create_company(company: schemas.CompanyCreate,current_user_email=Depends(auth_handler.get_current_user))->schemas.Company:
    company_crud = Company_Crud(get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    return await company_crud.create_company(company=company,user=user)