from typing import List
from utils.models import Answer, HistoricalAnswer
from utils.exceptions import ItemNotFoundError
from db.data_access import get_questions, insert_answer, update_customer_last_answers, get_customer
from utils.answer_validator import validate_answer


def insert_customer_answers(customer_id: int, answers: List[Answer]):
    questions = get_questions()

    customer = get_customer(customer_id)
    if customer is None:
        raise ItemNotFoundError(f'There is no customer with customer_id {customer_id} in db')

    historical_answers: List[HistoricalAnswer] = []
    for answer in answers:
        validate_answer(answer, questions)
        historical_answers.append(HistoricalAnswer(question_id=answer.question_id, customer_id=customer_id,
                                                   value=answer.value))

    for historical_answer in historical_answers:
        insert_answer(historical_answer)

    update_customer_last_answers(customer_id, answers)
