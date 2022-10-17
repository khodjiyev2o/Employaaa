from fastapi import APIRouter,Depends,Response
from users import database,schemas,crud,models
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from users.hashing import Hash
from utils import VerifyToken
from fastapi.security import HTTPBearer
router = APIRouter(
     tags=["authentication"],
)
token_auth_scheme = HTTPBearer()

@router.post("/login")
def login(
    response:Response,
    request : schemas.UserSignIn,
    token:str = Depends(token_auth_scheme),
    db:Session = Depends(database.get_db
    ))->models.User:

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid email")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password")

    ## generate jwt token and return
    result =VerifyToken(token.credentials).verify() 
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        resp = f"{response}does not match the token"
        return resp

    return user
    