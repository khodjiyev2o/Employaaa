from fastapi import APIRouter,Depends,Response
from users import database,schemas,crud,models
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from users.hashing import Hash
from fastapi.security import HTTPBearer
from utils import Token
router = APIRouter(
     tags=["authentication"],
)
token_auth_scheme = HTTPBearer()


@router.post("/login")
def login(response:Response,
    request : schemas.UserSignIn,
    token:str = Depends(token_auth_scheme),
    db:Session = Depends(database.get_db
    ))->schemas.User:

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid email")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password")

    ## verify the token
    if Token.access_token == token:
        return user    
    else:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid access_token") 
    
    