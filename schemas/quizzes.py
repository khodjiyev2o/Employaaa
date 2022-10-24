from typing import Optional
from pydantic import BaseModel,conlist


class Question(BaseModel):
      id: int
      question:str
      quiz_id:int
      answer:str
      options:conlist(list[str], min_items=2)
      

      class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
      question:str
      quiz_id:int
      answer:str
      options:conlist(list[str], min_items=2)
      

      class Config:
        orm_mode = True


class Quiz(BaseModel):
    name: str
    description: Optional[str]
    frequency:int

   

    class Config:
        orm_mode = True

class QuizOut(Quiz):
    id:int
    questions: conlist(list[Question], min_items=2)
   

    class Config:
        orm_mode = True


