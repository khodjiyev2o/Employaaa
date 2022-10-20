from fastapi import APIRouter,Depends,HTTPException,status
from typing import  List
from users import database,schemas,models
from sqlalchemy.orm import Session
from users.crud import Crud

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db



@router.get("/all/", response_model=List[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100)->List[schemas.User]:
    crud = Crud(get_db)
    return await crud.get_all_users(skip=skip, limit=limit)


    
@router.post("/create/",response_model=schemas.User)
async def create_user(user: schemas.UserSignUp)->schemas.User:
    crud = Crud(get_db)
    return await crud.create_user(user=user)


@router.put("/update/{id}", response_model=schemas.User)
async def get_user_by_id(id: int,user:schemas.UserUpdate)->schemas.User:
    crud = Crud(get_db)
    return await crud.update_user(user=user,id=id)



@router.get("/{id}", response_model=schemas.User)
async def get_user_by_id(id: int)->schemas.User:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_id(id=id)
    return db_user



@router.get("/{email}/",response_model=schemas.User)
async def get_user_by_email(email: str)->schemas.User:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete/{id}")
async def delete(id: int,user:schemas.User)->str:
    crud = Crud(get_db)
    db_user = await crud.get_user_by_id(id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")    
    return await crud.delete_user(id=id)








