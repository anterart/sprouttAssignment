from enum import Enum


class QuestionType(Enum):
    TEXT = 'text'
    NUMBER = 'number'
    DROPDOWN = 'dropdown'
    YES_NO = 'yes_no'


class FollowUpConditionOperator(Enum):
    EQUALS = 'equals'
    NOT_EQUALS = 'not_equals'
    LESS_THAN = 'less_than'
    LESS_THAN_EQ = 'less_than_eq'
    GREATER_THAN_EQ = 'greater_than_eq'
    GREATER_THAN = 'greater_than'
    ISIN = 'isin'
    NOTIN = 'notin'


class YesNoQuestion(Enum):
    YES = 'yes'
    NO = 'no'
