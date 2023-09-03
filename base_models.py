from pydantic import BaseModel
from typing import Optional


class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone: str


class FollowUpQuestion(BaseModel):
    main_question_id: int
    follow_up_question_id: int
    condition_operator: str
    condition_right_operand: str


class QuestionOption(BaseModel):
    option_id: int
    question_id: int
    position: int


class Option(BaseModel):
    option_id: int
    value: str


class Answer(BaseModel):
    question_id: int
    value: Optional[str]


class Question(BaseModel):
    question_id: int
    text: str
    question_type: str
    position: Optional[int] = None
