from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel



class Member(BaseModel):
    id: int
    company_id: int
    user_id: int
    is_admin: Optional[bool] = False
   

    class Config:
        orm_mode = True

class MemberInvite(BaseModel):
    company_id: int
    user_id: int
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True

class MemberOut(BaseModel):
    id:int
    user_id: int
    company_id : int
    is_admin: Optional[bool] = False  
    
class MemberDelete(BaseModel):
    user_id: int
    company_id : int


class MemberUpdate(BaseModel):
    user_id: int
    company_id : int
    is_admin : bool = False


class MemberwithTime(BaseModel):
    user_id: int
    last_time_solved: Optional[datetime]    