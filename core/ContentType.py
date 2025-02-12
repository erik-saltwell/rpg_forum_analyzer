from enum import Enum


class ContentType(int, Enum):
    OTHER = 0
    RULES_QUESTION = 1
    SCENARIO_DESIGN = 2
    PRODUCT_REVIEW = 3
    SHOW_AND_TELL = 4
