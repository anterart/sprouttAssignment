from db import data
from models import Customer, Question, HistoricalAnswer, Answer
from typing import Dict, List


def get_customer(customer_id: int) -> Customer:
    return data.customers.get(customer_id)


def get_questions() -> Dict[int, Question]:
    return data.questions


def get_next_answer_id() -> int:
    return len(data.historical_answers)


def insert_answer(answer: HistoricalAnswer):
    answer_id = get_next_answer_id()
    data.historical_answers[answer_id] = answer


def update_customer_last_answers(customer_id: int, answers: List[Answer]):
    for answer in answers:
        data.customers[customer_id].last_answers[answer.question_id] = answer


def get_stored_answers() -> Dict[int, HistoricalAnswer]:
    return data.historical_answers
