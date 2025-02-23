from enum import Enum


class ContentType(int, Enum):
    OTHER = 0
    RULES_QUESTION = 1
    SCENARIO_DESIGN = 2
    PRODUCT_REVIEW = 3
    SHOW_AND_TELL = 4
    ADVENTURE_QUESTION = 5


def to_simple_string(x: ContentType) -> str:
    if x == ContentType.OTHER:
        return "Other"
    if x == ContentType.RULES_QUESTION:
        return "Rules"
    if x == ContentType.SCENARIO_DESIGN:
        return "Scenario"
    if x == ContentType.PRODUCT_REVIEW:
        return "Product Review"
    if x == ContentType.SHOW_AND_TELL:
        return "Show & Tell"
    return "Adventure"
