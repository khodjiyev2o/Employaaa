
from typing import Optional
from email_validator import validate_email
from pydantic import BaseModel, ValidationError, validator,HttpUrl


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
    password: str
    
    class Config:
        orm_mode = True

class UserSignIn(BaseModel):
    email:str
    password:str

    class Config:
        orm_mode = True


class UserSignUp(User):
    first_name:Optional[str]
    email:str
    password:str
<<<<<<< HEAD:users/schemas.py
    confirm_password:str  
=======
    confirm_password:str
>>>>>>> 754d8bb2f3d4eedac68fb4fb964c1716fbec3675:schema.py
    phone_number: Optional[int]

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str] 
    email: Optional[str] 
    phone_number: Optional[int] 
    
    class Config:
        orm_mode = True




 
