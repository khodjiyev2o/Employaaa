from fastapi import APIRouter,Depends,HTTPException,status

from users import database,schemas,crud 

from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db









@router.post('/create_users',response_model=schemas.UserSignUp)
def create_user(request: schemas.UserSignUp,db: Session = Depends(get_db)):
    return crud.create_user(request,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update(id,request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return crud.destroy(db,id)


@router.get('/{email}')
def get_user_by_email(email:str,db: Session = Depends(get_db)):
    return crud.get_user_by_email(db,email) 


@router.get('/{id}')
def get_user(id:int,db: Session = Depends(get_db)):
    return crud.get_user_by_id(id,db)   



@router.get('/')
def all(db: Session = Depends(get_db)):
    return crud.get_users(db)