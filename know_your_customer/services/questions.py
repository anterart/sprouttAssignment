from db import data
from typing import Dict, List
from know_your_customer.api_models import Question
from base_models import Answer
from know_your_customer.services.answers import get_answers
from enums import QuestionType


def get_questions(customer_id: int) -> List[Question]:
    questions: List[Question] = [Question(**question.dict()) for question in data.questions]
    question_id_to_answer: Dict[int, Answer] = get_answers(customer_id)
    option_id_to_val: Dict[int, str] = {option.option_id: option.value for option in data.options}

    get_answer_options(questions)
    get_answer_value(question_id_to_answer, questions)
    get_selected_answer_index(option_id_to_val, question_id_to_answer, questions)
    get_follow_up_question_ids(questions)
    get_is_follow_up_question(questions)

    return questions


def get_is_follow_up_question(questions):
    for follow_up_question in data.follow_up_questions:
        follow_up_question_id = follow_up_question.follow_up_question_id
        questions[follow_up_question_id].is_follow_up = True


def get_follow_up_question_ids(questions):
    for follow_up_question in data.follow_up_questions:
        main_question_id = follow_up_question.main_question_id
        follow_up_question_id = follow_up_question.follow_up_question_id
        questions[main_question_id].follow_up_question_ids.append(follow_up_question_id)


def get_selected_answer_index(option_id_to_val, question_id_to_answer, questions):
    for question_id, answer in question_id_to_answer.items():
        question = questions[question_id]
        if question.question_type == QuestionType.DROPDOWN.value:
            selected_answer_index = question.answer_options.index(option_id_to_val[answer.option_id])
            question.selected_answer_index = selected_answer_index


def get_answer_value(question_id_to_answer, questions):
    for question_id, answer in question_id_to_answer.items():
        question = questions[question_id]
        question.answer_value = answer.value


def get_answer_options(questions):
    for question_options in data.question_options:
        question = questions[question_options.question_id]
        answer_value = data.options[question_options.option_id].value
        question.answer_options.append(answer_value)


