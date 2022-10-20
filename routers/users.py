from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from schemas import users as schemas
from users import database
from users.crud import Crud
from authentication.auth import AuthHandler


auth_handler = AuthHandler()
router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db



@router.get("/all/", response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100,user_email=Depends(auth_handler.auth_wrapper))->List[schemas.User]:
    crud = Crud(get_db)
    return await crud.get_all_users(skip=skip, limit=limit)


    
@router.post("/create/",response_model=schemas.User)
async def create_user(user: schemas.UserSignUp)->schemas.User:
    crud = Crud(get_db)
    return await crud.create_user(user=user)


@router.put("/update/{id}", response_model=schemas.User)
async def update_user(id: int,user:schemas.UserUpdate,user_email=Depends(auth_handler.auth_wrapper))->schemas.User:
    crud = Crud(get_db)
    return await crud.update_user(user=user,id=id)



@router.get("/{id}", response_model=schemas.User,)
async def get_user_by_id(id: int,user_email=Depends(auth_handler.auth_wrapper))->schemas.User:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_id(id=id)
    return db_user



@router.get("/{email}/",response_model=schemas.User)
async def get_user_by_email(email: str,user_email=Depends(auth_handler.auth_wrapper))->schemas.User:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete/{id}")
async def delete(id: int,user:schemas.User,user_email=Depends(auth_handler.auth_wrapper))->str:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_id(id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")    
    return await crud.delete_user(id=id)








