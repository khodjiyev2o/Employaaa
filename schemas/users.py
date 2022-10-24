from typing import Optional,List
from pydantic import BaseModel, validator,HttpUrl
from .invites import InviteOut

class Image(BaseModel):
    url: HttpUrl
    name: str
        
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[int] 
    email: str
    invite:Optional[List[InviteOut]]
  
         
    class Config:
        orm_mode = True

class UserSignIn(BaseModel):
    email:str
    password:str

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    email:str
    password:str
    confirm_password:str  
    phone_number: Optional[int]
    company_name: Optional[str]

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str] 
    password:Optional[str] 
    
    class Config:
        orm_mode = True




 
