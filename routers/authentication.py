from fastapi import APIRouter,Depends,Response
from users import database,schemas,crud,models
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from users.hashing import Hash
from fastapi.security import HTTPBearer
from utils import Token
from users.auth import AuthHandler
import os
from users.crud import Crud


router = APIRouter(
     tags=["authentication"]
)
token_auth_scheme = HTTPBearer()
auth_handler = AuthHandler()

@router.post("/login")
def login(
    request : schemas.UserSignIn,
    db:Session = Depends(database.get_db),
    )->schemas.User:

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user :
        crud = Crud(db=db)
        return crud.create_user(request)

    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password")
    
    ## encode the token
    token = auth_handler.encode_token(request.email)
    
    return user 
 

    
    