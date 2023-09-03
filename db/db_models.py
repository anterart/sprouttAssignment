from base_models import Answer as BaseAnswer
from typing import Optional
from datetime import datetime


class Answer(BaseAnswer):
    answer_id: int
    customer_id: int
    value: Optional[str] = None
    option_id: Optional[int] = None
    datetime_submitted: Optional[datetime] = datetime.now()
