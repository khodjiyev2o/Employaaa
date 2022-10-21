from typing import Optional,List
from pydantic import BaseModel


class Company(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str]
    supe_users: Optional[List[int]]
    members: Optional[List[int]]
    visible:bool = True
    
    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
      name: str
      description: Optional[str]

      class Config:
        orm_mode = True



class CompanyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str] 
    visible:Optional[bool] 

    class Config:
        orm_mode = True










