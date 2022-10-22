from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import companies as schemas
from schemas import members as member_schemas
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


@router.get("/get-all/", response_model=List[schemas.Company])
async def get_all_companies(skip: int = 0, limit: int = 100,current_user_email=Depends(auth_handler.get_current_user))->List[schemas.Company]:
    crud = Company_Crud(get_db)
    return await crud.get_all_companies(skip=skip, limit=limit)


@router.post("/create/",response_model=schemas.Company)
async def create_company(company: schemas.CompanyCreate,current_user_email=Depends(auth_handler.get_current_user))->schemas.Company:
    company_crud = Company_Crud(get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    return await company_crud.create_company(company=company,user=user)


@router.patch("/update/{id}",response_model=schemas.Company)
async def update_company(id:int,company: schemas.CompanyUpdate,current_user_email=Depends(auth_handler.get_current_user))->schemas.Company:
    company_crud = Company_Crud(get_db)
    active_company = await company_crud.get_company_by_id(id=id)
    if not active_company:
        raise HTTPException(status_code=404, detail=f"Company with name {id} not found")
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    if user.id != active_company.owner_id:
        raise  HTTPException(status_code=403, detail="User is not authorized to update another user's company!")
    return await company_crud.update_company(company=company,id=id)

@router.delete("/delete/{id}")
async def delete_company(id: int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    company_crud = Company_Crud(get_db)
    active_company = await company_crud.get_company_by_id(id=id)
    if not active_company:
        raise HTTPException(status_code=404, detail=f"Company with name {id} not found")
    current_user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    if current_user.id != active_company.owner_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's company!")
    return await company_crud.delete_company(id=id)

@router.get("/{name}/",response_model=schemas.Company)
async def get_company_by_name(name: str,user_email=Depends(auth_handler.auth_wrapper))->schemas.Company:
    crud = Company_Crud(get_db)
    company = await crud.get_company_by_name(name=name)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/invite/user/",response_model=member_schemas.Member)
async def invite_user(member: member_schemas.MemberInvite,current_user_email=Depends(auth_handler.get_current_user))->member_schemas.Member:
    company_crud = Company_Crud(get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    company = await company_crud.get_company_by_id(id=member.company_id)
    if user.id != company.owner_id:
        raise  HTTPException(status_code=403, detail="User is not authorized to invite other users to this company!")
    return await company_crud.invite_user(member)


@router.get("/get-all/members", response_model=List[member_schemas.Member])
async def get_all_members(skip: int = 0, limit: int = 100)->List[member_schemas.Member]:
    crud = Company_Crud(get_db)
    return await crud.get_members(skip=skip, limit=limit)
