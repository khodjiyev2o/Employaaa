from typing import Optional,List
from pydantic import BaseModel, validator,HttpUrl
from .invites import InviteOut


class Result(BaseModel):
    id: int
    company_id: int
    quiz_id: int
    user_id: int 
    result: int

class ResultCreate(BaseModel):
    company_id: int
    quiz_id: int
    user_id: int 
    result: int


class UserResult(BaseModel):
    company_id: int
    quiz_id: int
    result: int


class QuizResult(BaseModel):
    company_id: int
    user_id: int 
    result: int
    

