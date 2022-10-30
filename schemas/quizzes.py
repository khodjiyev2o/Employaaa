from pickletools import int4
from typing import Optional
from pydantic import BaseModel,conlist

from database.models import Base
from .results import QuizResult







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
    id: int
    name: str
    description: Optional[str]
    frequency:int
    company_id : int


    class Config:
        orm_mode = True

class QuizCreate(Quiz):
    name: str
    description: Optional[str]
    frequency:int
    company_id : int
    questions: conlist(Question, min_items=2)

    class Config:
        orm_mode = True

class QuizOut(Quiz):
    questions: conlist(Question, min_items=2)
    result: Optional[list[QuizResult]]

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    frequency:Optional[int]
    company_id : Optional[int]

    class Config:
        orm_mode = True

class Answer(BaseModel):
    question_id: int
    answer: str

        ##answer sheet :
class AnswerSheet(BaseModel):
    quiz_id: int
    answers: Optional[list[Answer]]


   



