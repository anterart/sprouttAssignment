from typing import Optional, List
from base_models import Question as BaseQuestion, Customer
from pydantic import BaseModel


class Question(BaseQuestion):
    answer_options: Optional[List[str]] = []
    selected_answer_index: Optional[int] = None
    follow_up_question_ids: Optional[List[int]] = []
    answer_value: Optional[str] = None
    is_follow_up: bool = False


class Questionnaire(BaseModel):
    customer: Customer
    questions: List[Question]
