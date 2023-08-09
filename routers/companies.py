from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import companies as schemas
from schemas import members as member_schemas

from repositories.companies import Company_Crud  
from repositories.users import User_Crud 
from authentication.auth import AuthHandler
from schemas import invites as invite_schemas
from database.database import database as get_db


auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}},
)



@router.get("/get-all/", response_model=List[schemas.Company])
async def get_all_companies(skip: int = 0, limit: int = 100,current_user_email=Depends(auth_handler.get_current_user))->List[schemas.Company]:
    crud = Company_Crud(db=get_db)
    return await crud.get_all_companies(skip=skip, limit=limit)


@router.post("/create/",response_model=schemas.Company)
async def create_company(company: schemas.CompanyCreate,current_user_email=Depends(auth_handler.get_current_user))->schemas.Company:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    return await company_crud.create_company(company=company,user=user)


@router.patch("/update/{id}",response_model=schemas.Company)
async def update_company(id:int,company: schemas.CompanyUpdate,current_user_email=Depends(auth_handler.get_current_user))->schemas.Company:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=id,user_id=user.id)
    if owner is True:
        return await company_crud.update_company(company=company,id=id)



@router.delete("/delete/{id}")
async def delete_company(id: int,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner =  await company_crud.check_for_owner(company_id=id,user_id=user.id)
    if owner is True:
        return await company_crud.delete_company(id=id)

@router.get("/{name}/",response_model=schemas.Company)
async def get_company_by_name(name: str,user_email=Depends(auth_handler.auth_wrapper))->schemas.Company:
    crud = Company_Crud(db=get_db)
    company = await crud.get_company_by_name(name=name)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company



@router.get("/get-all/members", response_model=List[member_schemas.Member])
async def get_all_members(skip: int = 0, limit: int = 100)->List[member_schemas.Member]:
    crud = Company_Crud(db=get_db)
    return await crud.get_members(skip=skip, limit=limit)  



##invite the user
@router.post("/invite/user/",response_model=invite_schemas.Invite)
async def invite_user(invite: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->invite_schemas.Invite:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=invite.company_id,user_id=user.id)
    if owner is True:
        return await company_crud.invite_user(invite)



@router.delete("/delete/member/")
async def delete_member(member:member_schemas.MemberDelete,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=member.company_id,user_id=user.id)
    if owner is True:
        return await company_crud.de(member=member)



#accept the user's application 
@router.post("/accept/user/",response_model=member_schemas.MemberOut)
async def accept_user(application: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->member_schemas.MemberOut:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=application.company_id,user_id=user.id)
    if owner is True:
        return await company_crud.accept_user(application)


@router.post("/update/admin/")
async def update_admin(member: member_schemas.MemberUpdate,current_user_email=Depends(auth_handler.get_current_user))->member_schemas.Member:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=member.company_id,user_id=user.id)
    if owner is True:
        return await company_crud.update_admin(member=member)


##decline the user's application

@router.post("/refuse/user")
async def refuse_user(invite: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = User_Crud(db=get_db)
    company_crud = Company_Crud(db=get_db)
    user = await crud.get_user_by_email(email=current_user_email)
    owner = await company_crud.check_for_owner(company_id=invite.company_id,user_id=user.id)
    if owner is True:
        return await crud.decline_invite(invite=invite)


@router.get("/get_members/time_solved")
async def get_members_time_solved(company_id: int,user_email=Depends(auth_handler.auth_wrapper))->List[member_schemas.MemberwithTime]:
    company_crud = Company_Crud(db=get_db)
    user = await User_Crud(db=get_db).get_user_by_email(email=user_email)
    owner = await company_crud.check_for_owner(company_id=company_id,user_id=user.id)
    if owner is True:
        print("i am inside crud functionality")
        return await company_crud.get_members_with_time(company_id=company_id)



@router.get("/total_mean_result_off_all")
async def get_members_time_solved(skip: int = 0, limit: int = 100)->int:
    company_crud = Company_Crud(db=get_db)
    return await company_crud.total_mean_result_off_all()












