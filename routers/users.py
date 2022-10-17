from fastapi import APIRouter,Depends,HTTPException,status

from users import database,schemas,crud ,models

from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db









@router.post('/create_users',response_model=schemas.User)
def create_user(request: schemas.UserSignUp,db: Session = Depends(get_db))->schemas.User:
    return crud.create_user(request,db)

@router.put('/{id}',response_model=schemas.User,status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.UserUpdate, db: Session = Depends(get_db))->schemas.User:
    return crud.update(id=id,request=request, db=db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return crud.destroy(db=db,id=id)


@router.get('/email/{email}',response_model=schemas.User)
def get_user_by_email(email:str,db: Session = Depends(get_db))->schemas.User:
    return crud.get_user_by_email(db=db,email=email) 


@router.get('/{id}',response_model=schemas.User)
def get_user(id:int,db: Session = Depends(get_db))->schemas.User:
    return crud.get_user_by_id(id,db)   



@router.get('/')
def all(db: Session = Depends(get_db))->schemas.User:
    return crud.get_users(db)