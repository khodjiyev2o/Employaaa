from typing import Optional
from pydantic import BaseModel

from schemas.companies import Company
from .members import MemberOut




class Invite(BaseModel):
    id: int
    user_id: int
    company_id:int
    
    class Config:
        orm_mode = True





class InviteCreate(BaseModel):
    user_id: int
    company_id:int
    
    class Config:
        orm_mode = True


class InviteOut(BaseModel):
    company_id:int

    class Config:
        orm_mode = True