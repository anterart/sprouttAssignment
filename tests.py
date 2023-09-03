from fastapi.testclient import TestClient
from main import app
from models import Answer, Questionnaire
from enums import YesNoQuestion
from typing import List, Dict
from db.data_access import get_stored_answers

client = TestClient(app)


def get_answers_values(question_ids: List[int], questionnaire: Questionnaire) -> List[str]:
    answers_values = []
    for question in questionnaire['questions'].values():
        if question['question_id'] in question_ids:
            answers_values.append(question['answer_value'])
    return answers_values


def get_new_answers() -> List[Answer]:
    new_answers = [
        Answer(question_id=0, value="37"),
        Answer(question_id=1, value=YesNoQuestion.NO.value),
        Answer(question_id=4, value='5555555'),
        Answer(question_id=5, value=YesNoQuestion.YES.value),
        Answer(question_id=6, value=YesNoQuestion.YES.value),
        Answer(question_id=7, value='Other'),
        Answer(question_id=9, value='programmer')
    ]
    return new_answers


def get_question_id_to_answer(answers: List[Answer]) -> Dict[int, Answer]:
    answers_dict = {}
    for answer in answers:
        answers_dict[answer.question_id] = answer

    return answers_dict


def test_get_questionnaire1():
    """
    Should return the questionnaire for customer_id = 0, this customer already completed the questionnaire so we expect
     to see his answers.
    """
    response = client.get("/get_questionnaire", params={"customer_id": 0})
    assert response.status_code == 200
    num_questions = 10
    questions = response.json()['questions']
    assert len(questions) == num_questions
    assert response.json() == {'customer': {'customer_id': 0, 'first_name': 'Leonidas', 'last_name': 'I', 'email': 'king@sparta.gr', 'phone': '123456', 'last_answers': {'0': {'question_id': 0, 'value': '50'}, '1': {'question_id': 1, 'value': 'yes'}, '2': {'question_id': 2, 'value': 'Term'}, '3': {'question_id': 3, 'value': '77777'}, '5': {'question_id': 5, 'value': 'no'}, '9': {'question_id': 9, 'value': 'Au! Au! Au!'}}}, 'questions': {'0': {'question_id': 0, 'text': 'At what age do you plan to retire?', 'question_type': 'number', 'position': 0, 'options': [], 'follow_up_questions': [], 'is_follow_up': False, 'answer_value': '50', 'dropdown_data': None}, '1': {'question_id': 1, 'text': 'Do you currently have any life insurance coverage?', 'question_type': 'yes_no', 'position': 1, 'options': [], 'follow_up_questions': [{'follow_up_question_id': 2, 'condition_operator': 'equals', 'condition_second_operand': 'yes'}, {'follow_up_question_id': 3, 'condition_operator': 'equals', 'condition_second_operand': 'yes'}, {'follow_up_question_id': 4, 'condition_operator': 'equals', 'condition_second_operand': 'no'}], 'is_follow_up': False, 'answer_value': 'yes', 'dropdown_data': None}, '2': {'question_id': 2, 'text': 'What is the type of life insurance?', 'question_type': 'dropdown', 'position': 0, 'options': ['Term', 'Whole Life', 'UL', 'IUL', 'VUL', 'Other'], 'follow_up_questions': [], 'is_follow_up': True, 'answer_value': 'Term', 'dropdown_data': {'options': ['Term', 'Whole Life', 'UL', 'IUL', 'VUL', 'Other'], 'chosen_option_index': 0}}, '3': {'question_id': 3, 'text': 'What is the amount?', 'question_type': 'number', 'position': 1, 'options': [], 'follow_up_questions': [], 'is_follow_up': True, 'answer_value': '77777', 'dropdown_data': None}, '4': {'question_id': 4, 'text': 'What is the amount you are looking for?', 'question_type': 'number', 'position': 2, 'options': [], 'follow_up_questions': [], 'is_follow_up': True, 'answer_value': None, 'dropdown_data': None}, '5': {'question_id': 5, 'text': 'Do you have any dependents?', 'question_type': 'yes_no', 'position': 2, 'options': [], 'follow_up_questions': [{'follow_up_question_id': 6, 'condition_operator': 'equals', 'condition_second_operand': 'yes'}], 'is_follow_up': False, 'answer_value': 'no', 'dropdown_data': None}, '6': {'question_id': 6, 'text': 'Does any of your dependents have a chronic disease?', 'question_type': 'yes_no', 'position': 0, 'options': [], 'follow_up_questions': [{'follow_up_question_id': 6, 'condition_operator': 'equals', 'condition_second_operand': 'yes'}], 'is_follow_up': True, 'answer_value': None, 'dropdown_data': None}, '7': {'question_id': 7, 'text': 'Which chronic disease does your dependent have?', 'question_type': 'dropdown', 'position': 0, 'options': ['Diabetes', 'Heart Disease', 'Cancer', 'Other'], 'follow_up_questions': [], 'is_follow_up': True, 'answer_value': None, 'dropdown_data': None}, '8': {'question_id': 8, 'text': 'What is your favorite joke?', 'question_type': 'text', 'position': 3, 'options': [], 'follow_up_questions': [], 'is_follow_up': False, 'answer_value': None, 'dropdown_data': None}, '9': {'question_id': 9, 'text': 'What is your profession?', 'question_type': 'text', 'position': None, 'options': [], 'follow_up_questions': [], 'is_follow_up': False, 'answer_value': 'Au! Au! Au!', 'dropdown_data': None}}}


def test_get_questionnaire2():
    """
    Get questionnaire for customer that didnt answer any questions yet. We will expect that all the answers values will
     be None
    """
    response = client.get("/get_questionnaire", params={"customer_id": 1})
    assert response.status_code == 200
    num_questions = 10
    questions = response.json()['questions']
    assert len(questions) == num_questions
    for out_question in questions.values():
        assert out_question['answer_value'] is None
        assert out_question['dropdown_data'] is None


def test_non_existing_get_questionnaire():
    response = client.get("/get_questionnaire", params={"customer_id": 5})
    assert response.status_code == 404


def test_inserting_answers_persistence():
    new_answers = get_new_answers()
    customer_id = 2
    response = client.get("/get_questionnaire", params={"customer_id": customer_id})
    question_ids = [a.question_id for a in new_answers]
    actual = get_answers_values(question_ids, response.json())
    expected = [None] * len(new_answers)
    assert actual == expected
    assert response.status_code == 200

    response = client.post(f'/save_answers/{customer_id}', json=[answer.model_dump() for answer in new_answers])
    assert response.status_code == 200

    response = client.get("/get_questionnaire", params={"customer_id": customer_id})
    expected = [new_answers[i].value for i in range(len(new_answers))]
    actual = get_answers_values(question_ids, response.json())
    assert actual == expected
    assert response.status_code == 200


def test_insert_answers_valid1():
    """
    Try to insert non-numeric answer to numeric question
    """
    new_answers = [
        {'question_id': 0, 'value': 'a'},
    ]
    customer_id = 2
    response = client.post(f'/save_answers/{customer_id}', json=new_answers)
    assert response.status_code == 500


def test_insert_answers_valid2():
    """
    Try to insert non-no/yes answer to no/yes question
    """
    new_answers = [
        {'question_id': 1, 'value': 'a'},
    ]
    customer_id = 2
    response = client.post(f'/save_answers/{customer_id}', json=new_answers)
    assert response.status_code == 500


def test_insert_answers_valid3():
    """
    Try to insert non-existing answer to dropdown question
    """
    new_answers = [
        {'question_id': 2, 'value': 'a'},
    ]
    customer_id = 2
    response = client.post(f'/save_answers/{customer_id}', json=new_answers)
    assert response.status_code == 500


def test_insert_answers_valid4():
    """
    Try to insert answer to non-existing question
    """
    new_answers = [
        {'question_id': 200, 'value': 'a'},
    ]
    customer_id = 2
    response = client.post(f'/save_answers/{customer_id}', json=new_answers)
    assert response.status_code == 500


def test_answers_storing():
    """
    Check if all submitted answers are stored
    """
    new_answers = get_new_answers()
    customer_id = 2

    stored_answers = get_stored_answers()
    assert len(stored_answers) == 0

    response = client.post(f'/save_answers/{customer_id}', json=[answer.model_dump() for answer in new_answers])
    assert response.status_code == 200

    stored_answers = get_stored_answers()
    assert len(stored_answers) == len(new_answers)

    answers_dict = get_question_id_to_answer(new_answers)

    for answer in stored_answers.values():
        assert answer.customer_id == customer_id
        new_answer = answers_dict[answer.question_id]
        assert new_answer.question_id == answer.question_id
        assert new_answer.value == answer.value
