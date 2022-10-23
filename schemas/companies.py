from typing import Optional
from pydantic import BaseModel
from .members import MemberOut

class Company(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str]
    visible:bool = True
    members: Optional[list[MemberOut]]
    
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










