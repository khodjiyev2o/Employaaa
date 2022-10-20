from email.policy import default
from typing import Optional,List
from pydantic import BaseModel, ValidationError, validator,HttpUrl
from .users import User

class Company(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str]
    super_users:Optional(List[User])
    members: Optional(List[User])
    visible:bool = True
    
    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
      id: int
      owner_id: int
      name: str

      class Config:
        orm_mode = True



class CompanyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str] 

    class Config:
        orm_mode = True

class CompanyOut(CompanyCreate):
    super_users:Optional(List[User])
    members: Optional(List[User])

    class Config:
        orm_mode = True





