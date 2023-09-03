from db import data
from typing import Dict, List
from base_models import Answer as InAnswer, Question
from db.db_models import Answer as DBAnswer
from exceptions import ItemNotFoundError, ValueDoesntFitToQuestionTypeError
from enums import QuestionType, YesNoQuestion


def get_answers(customer_id: int) -> Dict[int, DBAnswer]:
    answers: Dict[int, DBAnswer] = {}
    for answer in data.answers:
        if answer.customer_id != customer_id:
            continue

        if answer.question_id not in answers:
            answers[answer.question_id] = answer
            continue

        if answer.answer_id > answers[answer.question_id].answer_id:
            answers[answer.question_id] = answer

    return answers


def get_next_answer_id():
    if len(data.answers) == 0:
        return 0

    return data.answers[-1].answer_id + 1


def insert_answers(customer_id: int, answers: List[InAnswer]):
    question_id_to_questions: Dict[int, Question] = {question.question_id: question for question in data.questions}
    for answer in answers:
        option_id = get_answer_details(answer, question_id_to_questions)
        value = None if option_id else answer.value
        data.answers.append(DBAnswer(question_id=answer.question_id, customer_id=customer_id, value=value,
                                     option_id=option_id, answer_id=get_next_answer_id()))


def get_answer_details(answer, question_id_to_questions):
    if answer.question_id not in question_id_to_questions:
        raise ItemNotFoundError(f'There is no question for question_id {answer.question_id} for answer {answer}')
    option_id = None
    question = question_id_to_questions[answer.question_id]
    if question.question_type == QuestionType.NUMBER.value:
        validate_numeric_question_answer(answer)

    elif question.question_type == QuestionType.YES_NO.value:
        validate_yes_no_question_answer(answer)

    elif question.question_type == QuestionType.DROPDOWN.value:
        option_id = get_option_id_for_dropdown_question_answer(answer)

    return option_id


def get_option_id_for_dropdown_question_answer(answer):
    chosen_option_id = None
    for option in data.options:
        if answer.value == option.value:
            chosen_option_id = option.option_id

    if chosen_option_id is None:
        raise ValueDoesntFitToQuestionTypeError(f'{answer.value} cant be chosen for this question_id'
                                                f' {answer.question_id}')
    return chosen_option_id


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
