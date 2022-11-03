from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import users as schemas
from schemas import invites as invite_schemas
from schemas import results as result_schemas 
from repositories.users import User_Crud as Crud
from repositories.companies import Company_Crud as Company_Crud
from authentication.auth import AuthHandler
from schemas import members as member_schemas
from database.database import database as get_db

auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)




#USER ANALYTICS 
@router.get("/all-users/mean-result",response_model=List[result_schemas.AllUserMeanResult])
async def users_mean_results(skip: int = 0, limit: int = 100,user_email=Depends(auth_handler.auth_wrapper))->List[result_schemas.AllUserMeanResult]:
    crud = Crud(db=get_db)
    users = await crud.get_all_users_mean_result(skip=skip,limit=limit)
    return users 

@router.get('/get_user/mean_results/from_all_quizzes',response_model=List[result_schemas.UserMeanResultQuiz])
async def get_user_mean_results_from_all_quizzes(user_id:int,user_email=Depends(auth_handler.auth_wrapper))->List[result_schemas.Result]:
    crud = Crud(db=get_db)
    user = await crud.get_user_by_email(email=user_email)
    if user_id != user.id:
        raise HTTPException(status_code=403, detail="User is not authorized to get another user's account info!")
    results = await crud.get_user_mean_result_from_all_quizzes(user_id=user_id)
    return results 


@router.get('get_user/mean_result_from/each_quiz',response_model=List[result_schemas.UserMeanResultAllQuiz])
async def get_user_mean_result_from_each_quiz(user_id:int):
    crud = Crud(db=get_db)
    results = await crud.get_user_mean_result_from_each_quiz(user_id=user_id)
    return results 

@router.get("/all/", response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100)->List[schemas.User]:
    crud = Crud(db=get_db)
    return await crud.get_all_users(skip=skip, limit=limit)


    
@router.post("/create/",response_model=schemas.User)
async def create_user(user: schemas.UserSignUp)->schemas.User:
    crud = Crud(db=get_db)
    return await crud.create_user(user=user)


@router.patch("/update/{id}",response_model=schemas.User)
async def update_user(id: int,user:schemas.UserUpdate,current_user_email=Depends(auth_handler.get_current_user))->schemas.User:
    crud = Crud(db=get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    if current_user.id != id :
        raise  HTTPException(status_code=403, detail="User is not authorized to update another user's account!")
    return await crud.update_user(user=user,id=id)



@router.get("/{id}", response_model=schemas.User,)
async def get_user_by_id(id: int,user_email=Depends(auth_handler.auth_wrapper))->schemas.User:
    crud = Crud(db=get_db)
    db_user = await crud.get_user_by_id(id=id)
    return db_user



@router.get("/{email}/",response_model=schemas.User)
async def get_user_by_email(email: str,user_email=Depends(auth_handler.auth_wrapper))->schemas.User:
    crud = Crud(db=get_db)
    db_user = await crud.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete/{id}")
async def delete(id: int,user:schemas.User,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Crud(db=get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    if current_user.id != id :
        raise  HTTPException(status_code=403, detail="User is not authorized to delete another user's account!")
    return await crud.delete_user(id=id)
    


##apply to company
@router.post("/apply/company")
async def apply_to_company(application: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->invite_schemas.InviteOut:
    crud = Crud(db=get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    if current_user.id != application.user_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to apply as another user!")
    return await crud.apply_to_company(application=application)


##accept company's invite
@router.post("/accept/invite")
async def accept_invite(invite: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->member_schemas.MemberOut:
    crud = Crud(db=get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    if current_user.id != invite.user_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to accept another user's invite!")
    return await crud.accept_invite(invite=invite)
##decline the company's invite

@router.post("/decline/invite")
async def decline_invite(invite: invite_schemas.InviteCreate,current_user_email=Depends(auth_handler.get_current_user))->HTTPException:
    crud = Crud(db=get_db)
    current_user = await crud.get_user_by_email(email=current_user_email)
    if current_user.id != invite.user_id :
        raise  HTTPException(status_code=403, detail="User is not authorized to decline another user's invite!")
    return await crud.decline_invite(invite=invite)






