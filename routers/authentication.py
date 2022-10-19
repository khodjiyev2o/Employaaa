##importd from other modules
from fastapi import APIRouter,Depends,Response,HTTPException,status
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Response, status  
from fastapi.security import HTTPBearer


##imports from my modules
from users import database,schemas,crud,models
from users.hashing import Hash
from users.auth import AuthHandler
from users.crud import Crud



router = APIRouter(
     tags=["authentication"]
)
token_auth_scheme = HTTPBearer()
auth_handler = AuthHandler()

@router.post("/login")
def login(response: Response,
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
    #returns the generated token from user's email
    return token 
 

    
    