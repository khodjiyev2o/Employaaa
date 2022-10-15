from pydantic import BaseModel, HttpUrl
from typing import Optional
from email_validator import validate_email


class Image(BaseModel):
    url: HttpUrl
    name: str
        
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    phone_number: Optional[int] 
    email: str
    
    class Config:
        orm_mode = True

class UserSignIn(User):
    email:validate_email
    password:str

    class Config:
        orm_mode = True


class UserSignUp(User):
    first_name:str
    email:validate_email
    password:str
    phone_number: Optional[int]

    class Config:
        orm_mode = True

class UserUpdate(User):
    first_name: Optional[str] 
    email: Optional[validate_email] 
    phone_number: Optional[int] 
    
    class Config:
        orm_mode = True




 
