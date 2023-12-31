from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.questionnaire import get_questionnaire_obj
from services.answer import insert_customer_answers
from typing import List
from utils.models import Answer
from utils.exceptions import ValueDoesntFitToQuestionTypeError, ItemNotFoundError
from utils.consts import SAVE_ANSWERS_ENDPOINT, GET_QUESTIONNAIRE_ENDPOINT


app = FastAPI()


@app.get(GET_QUESTIONNAIRE_ENDPOINT)
def get_questionnaire(customer_id: int):
    try:
        questionnaire = get_questionnaire_obj(customer_id)
        return questionnaire
    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post(f"{SAVE_ANSWERS_ENDPOINT}/{'{customer_id}'}")
def save_answers(customer_id: int, answers: List[Answer]):
    try:
        insert_customer_answers(customer_id, answers)
    except (ValueDoesntFitToQuestionTypeError, ItemNotFoundError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content={"message": "The answers were inserted successfully"}, status_code=200)
