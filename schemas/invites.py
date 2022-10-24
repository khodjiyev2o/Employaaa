from typing import Optional
from pydantic import BaseModel





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


class ApplicatoCompany(BaseModel):
    user_id: int
    
    class Config:
        orm_mode = True