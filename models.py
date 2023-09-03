from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class FollowUpQuestion(BaseModel):
    follow_up_question_id: int
    condition_operator: str
    condition_second_operand: str


class Answer(BaseModel):
    question_id: int
    value: Optional[str]


class DropdownData(BaseModel):
    options: List[str]
    chosen_option_index: Optional[int] = None


class HistoricalAnswer(Answer):
    customer_id: int
    datetime_submitted: Optional[datetime] = datetime.now()


class Question(BaseModel):
    question_id: int
    text: str
    question_type: str
    position: Optional[int] = None
    options: Optional[List[str]] = []
    follow_up_questions: Optional[List[FollowUpQuestion]] = []
    is_follow_up: bool


class OutQuestion(Question):
    answer_value: Optional[str] = None
    dropdown_data: Optional[DropdownData] = None


class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    last_answers: Optional[Dict[int, Answer]] = {}


class Questionnaire(BaseModel):
    customer: Customer
    questions: Dict[int, OutQuestion]
