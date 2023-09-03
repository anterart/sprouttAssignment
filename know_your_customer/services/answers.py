from typing import List
from models import Answer, HistoricalAnswer
from exceptions import ItemNotFoundError, ValueDoesntFitToQuestionTypeError
from enums import QuestionType, YesNoQuestion
from db.data_access import get_questions, insert_answer, update_customer_last_answers, get_customer


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


def validate_answer(answer, questions):
    if answer.question_id not in questions:
        raise ItemNotFoundError(f'There is no question for question_id {answer.question_id} in db for answer {answer}')

    question = questions[answer.question_id]
    if question.question_type == QuestionType.NUMBER.value:
        validate_numeric_question_answer(answer)

    elif question.question_type == QuestionType.YES_NO.value:
        validate_yes_no_question_answer(answer)

    elif question.question_type == QuestionType.DROPDOWN.value:
        validate_answer_exists_in_options(answer, question)


def validate_answer_exists_in_options(answer, question):
    if answer.value is None:
        return

    if answer.value not in question.options:
        raise ValueDoesntFitToQuestionTypeError(f'{answer.value} cant be chosen for this question_id'
                                                f' {answer.question_id}')


def validate_yes_no_question_answer(answer):
    if answer.value not in {opt.value for opt in YesNoQuestion}:
        raise ValueDoesntFitToQuestionTypeError(f'{answer.value} is not of type {QuestionType.YES_NO.value} for'
                                                f' question_id {answer.question_id}')


def validate_numeric_question_answer(answer):
    try:
        float(answer.value)
    except ValueError:
        raise ValueDoesntFitToQuestionTypeError(f'{answer.value} is not of type {QuestionType.NUMBER.value} for'
                                                f' question_id {answer.question_id}')
