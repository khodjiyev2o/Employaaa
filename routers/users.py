from fastapi import APIRouter,Depends,HTTPException,status
from fastapi_pagination import Page
from users import database,schemas,crud ,models
from fastapi_pagination import Page,LimitOffsetPage,paginate,add_pagination
from sqlalchemy.orm import Session
from users.crud import Crud

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db








@router.post('/create_users')
async def create_user(request: schemas.UserSignUp,db: Session = Depends(get_db))->schemas.User:
    crud = Crud(db=db)
    return  crud.create_user(request)

@router.put('/{id}',response_model=schemas.User,status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.UserUpdate, db: Session = Depends(get_db))->schemas.User:
    crud = Crud(db=db)
    return crud.update(id=id,request=request)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db))->str:
    crud = Crud(db=db)
    return crud.destroy(id=id)


@router.get('/email/{email}',response_model=schemas.User)
def get_user_by_email(email:str,db: Session = Depends(get_db))->schemas.User:
    crud = Crud(db=db)
    return crud.get_user_by_email(email=email) 


@router.get('/{id}',response_model=schemas.User)
def get_user(id:int,db: Session = Depends(get_db))->schemas.User:
    crud = Crud(db=db)
    return crud.get_user_by_id(id)   



@router.get('/',response_model=Page[schemas.User])
@router.get("/limit-offset",response_model=LimitOffsetPage[schemas.User])
def all(db: Session = Depends(get_db))->schemas.User:
    crud = Crud(db=db)
    return paginate(crud.get_users())
add_pagination(router)