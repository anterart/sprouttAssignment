from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_answers_values(question_ids, questionnaire):
    answers_values = []
    for question in questionnaire['questions']:
        if question['question_id'] in question_ids:
            if question['selected_answer_index'] is not None:
                answers_values.append(question['answer_options'][question['selected_answer_index']])
            else:
                answers_values.append(question['answer_value'])
    return answers_values


def test_get_questionnaire1():
    """
    Should return the questionnaire for customer_id = 1, this customer already completed the questionnaire.
    """
    response = client.get("/get_questionnaire", params={"customer_id": 1})
    assert response.status_code == 200
    assert response.json() == {'customer': {'customer_id': 1, 'first_name': 'Arty', 'last_name': 'Abramovich', 'email': 'a@gmail.com', 'phone': '123456'}, 'questions': [{'question_id': 0, 'text': 'At what age do you plan to retire?', 'question_type': 'number', 'position': 0, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': '37', 'is_follow_up': False}, {'question_id': 1, 'text': 'Do you currently have any life insurance coverage?', 'question_type': 'yes_no', 'position': 1, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [2, 3, 4], 'answer_value': 'no', 'is_follow_up': False}, {'question_id': 2, 'text': 'What is the type of life insurance?', 'question_type': 'dropdown', 'position': 0, 'answer_options': ['Term', 'Whole Life', 'UL', 'IUL', 'VUL', 'Other'], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 3, 'text': 'What is the amount?', 'question_type': 'number', 'position': 1, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 4, 'text': 'What is the amount you are looking for?', 'question_type': 'number', 'position': 2, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': '5555555', 'is_follow_up': True}, {'question_id': 5, 'text': 'Do you have any dependents?', 'question_type': 'yes_no', 'position': 2, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [6, 7], 'answer_value': 'yes', 'is_follow_up': False}, {'question_id': 6, 'text': 'Does any of your dependents have a chronic disease?', 'question_type': 'yes_no', 'position': 0, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': 'yes', 'is_follow_up': True}, {'question_id': 7, 'text': 'Which chronic disease does your dependent have?', 'question_type': 'dropdown', 'position': 0, 'answer_options': ['Diabetes', 'Heart Disease', 'Cancer', 'Other'], 'selected_answer_index': 3, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 8, 'text': 'What is your favorite joke?', 'question_type': 'text', 'position': 3, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': False}, {'question_id': 9, 'text': 'What is your profession?', 'question_type': 'text', 'position': None, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': 'programmer', 'is_follow_up': False}]}


def test_get_questionnaire2():
    """
    Should return the questionnaire for customer_id = 0, this customer already completed the questionnaire.
    """
    response = client.get("/get_questionnaire", params={"customer_id": 0})
    assert response.status_code == 200
    assert response.json() == {'customer': {'customer_id': 0, 'first_name': 'Leonidas', 'last_name': 'I', 'email': 'king@sparta.gr', 'phone': '123456'}, 'questions': [{'question_id': 0, 'text': 'At what age do you plan to retire?', 'question_type': 'number', 'position': 0, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': '60', 'is_follow_up': False}, {'question_id': 1, 'text': 'Do you currently have any life insurance coverage?', 'question_type': 'yes_no', 'position': 1, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [2, 3, 4], 'answer_value': 'yes', 'is_follow_up': False}, {'question_id': 2, 'text': 'What is the type of life insurance?', 'question_type': 'dropdown', 'position': 0, 'answer_options': ['Term', 'Whole Life', 'UL', 'IUL', 'VUL', 'Other'], 'selected_answer_index': 0, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 3, 'text': 'What is the amount?', 'question_type': 'number', 'position': 1, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': '77777', 'is_follow_up': True}, {'question_id': 4, 'text': 'What is the amount you are looking for?', 'question_type': 'number', 'position': 2, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 5, 'text': 'Do you have any dependents?', 'question_type': 'yes_no', 'position': 2, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [6, 7], 'answer_value': 'no', 'is_follow_up': False}, {'question_id': 6, 'text': 'Does any of your dependents have a chronic disease?', 'question_type': 'yes_no', 'position': 0, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 7, 'text': 'Which chronic disease does your dependent have?', 'question_type': 'dropdown', 'position': 0, 'answer_options': ['Diabetes', 'Heart Disease', 'Cancer', 'Other'], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': True}, {'question_id': 8, 'text': 'What is your favorite joke?', 'question_type': 'text', 'position': 3, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': None, 'is_follow_up': False}, {'question_id': 9, 'text': 'What is your profession?', 'question_type': 'text', 'position': None, 'answer_options': [], 'selected_answer_index': None, 'follow_up_question_ids': [], 'answer_value': 'Au! Au! Au!', 'is_follow_up': False}]}


def test_non_existing_get_questionnaire():
    response = client.get("/get_questionnaire", params={"customer_id": 5})
    assert response.status_code == 404


def test_insering_answers_persistance():
    new_answers = [
        {'question_id': 0, 'value': '40'},
        {'question_id': 1, 'value': 'yes'},
        {'question_id': 2, 'value': 'Term'}
    ]
    customer_id = 2
    response = client.get("/get_questionnaire", params={"customer_id": customer_id})
    question_ids = [a['question_id'] for a in new_answers]
    actual = get_answers_values(question_ids, response.json())
    expected = [None, None, None]
    assert actual == expected
    assert response.status_code == 200

    response = client.post(f'/save_answers/{customer_id}', json=new_answers)
    assert response.status_code == 200

    response = client.get("/get_questionnaire", params={"customer_id": customer_id})
    expected = [new_answers[i]['value'] for i in range(len(new_answers))]
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
