from models import Question, DropdownData, OutQuestion, Questionnaire
from typing import List
from enums import QuestionType
from exceptions import ItemNotFoundError
from db.data_access import get_customer, get_questions


def get_dropdown_data(options, answer_value) -> DropdownData:
    chosen_option_index = None
    if answer_value is not None:
        chosen_option_index = options.index(answer_value)
    return DropdownData(options=options, chosen_option_index=chosen_option_index)


def build_out_question(question: Question, answer_value) -> OutQuestion:
    dropdown_data = None
    if question.question_type == QuestionType.DROPDOWN.value:
        dropdown_data = get_dropdown_data(question.options, answer_value)
    return OutQuestion(**question.model_dump(), answer_value=answer_value, dropdown_data=dropdown_data)


def get_questionnaire_obj(customer_id: int) -> Questionnaire:
    customer = get_customer(customer_id)
    if not customer:
        raise ItemNotFoundError

    last_answers = customer.last_answers
    out_questions: List[OutQuestion] = []
    questions = get_questions()

    for question_id, question in questions.items():
        if question_id in last_answers:
            answer = last_answers[question_id]
            out_questions.append(build_out_question(question, answer.value))
        else:
            out_questions.append(OutQuestion(**question.model_dump()))

    questionnaire = Questionnaire(customer=customer, questions=out_questions)
    return questionnaire
