from utils.enums import QuestionType, YesNoQuestion
from utils.exceptions import ItemNotFoundError, ValueDoesntFitToQuestionTypeError


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
