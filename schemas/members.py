from typing import Optional,List
from pydantic import BaseModel

from database.models import Company




class Member(BaseModel):
    id: int
    company_id: int
    user_id: int
    is_admin: Optional[bool] = False
    #company: List[Company] = []



class MemberInvite(BaseModel):
    company_id: int
    user_id: int
    is_admin: Optional[bool] = False
  