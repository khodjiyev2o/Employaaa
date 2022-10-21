##importd from other modules
from fastapi import APIRouter,Depends,Response,HTTPException,status
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status  
from fastapi.security import HTTPBearer
from database.models import User
from schemas import users as schemas


##imports from my modules
from database import database
from users.hashing import Hash
from authentication.auth import AuthHandler




router = APIRouter(
     tags=["authentication"]
)
token_auth_scheme = HTTPBearer()
auth_handler = AuthHandler()

@router.post("/login")
def login(response: Response,
    request : schemas.UserSignIn,
    db:Session = Depends(database.get_db),
    )->str:

    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
                 raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password")
    
   
    ## encode the token
    token = auth_handler.encode_token(request.email)
    #returns the generated token from user's email
    return token 
 

    
    