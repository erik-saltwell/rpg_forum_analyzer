from processing.content_classifier import _convert_to_content_type
from processing.content_classifier import ContentType


def test_convert_to_content_type() -> None:
    assert _convert_to_content_type("rules are my hero") == ContentType.RULES_QUESTION
    assert _convert_to_content_type("PRODUCT REVIEW") == ContentType.PRODUCT_REVIEW
    assert _convert_to_content_type("design scenario") == ContentType.SCENARIO_DESIGN
    assert _convert_to_content_type("show and tell") == ContentType.SHOW_AND_TELL
    assert _convert_to_content_type("show") == ContentType.OTHER


def test_mult_type_convert_to_content_type() -> None:
    assert _convert_to_content_type("rules are my hero show and tell") == ContentType.OTHER
