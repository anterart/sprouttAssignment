from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from know_your_customer.services.customer import get_customer_details
from know_your_customer.services.questions import get_questions
from know_your_customer.services.answers import insert_answers
from know_your_customer.api_models import Questionnaire
from typing import List
from base_models import Answer
from exceptions import ValueDoesntFitToQuestionTypeError, ItemNotFoundError


app = FastAPI()


def get_customer_details_helper(customer_id):
    customer_details = get_customer_details(customer_id)
    if not customer_details:
        raise HTTPException(status_code=404, detail=f'Customer with id {customer_id} does not exist.')
    return customer_details


@app.get("/get_questionnaire")
def get_questionnaire(customer_id: int):
    customer_details = get_customer_details_helper(customer_id)

    questions = get_questions(customer_id)
    return Questionnaire(customer=customer_details, questions=questions)


@app.post("/save_answers/{customer_id}")
def save_answers(customer_id: int, answers: List[Answer]):
    get_customer_details_helper(customer_id)
    try:
        insert_answers(customer_id, answers)
    except (ValueDoesntFitToQuestionTypeError, ItemNotFoundError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"message": "The answers were inserted successfully"}, status_code=200)
