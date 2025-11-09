"""Test script for Hebrew-named Jinja filters."""

import pytest
from jinja2 import Environment

from hebrew_numbers.jinja import HebrewNumbersExtension


@pytest.mark.parametrize(
    ("template_str", "expected_result"),
    [
        ("{{ 5 | מספר_סתמי }}", "חמש"),
        ("{{ 3 | מספר_מונה('נ', 'נפרד') }}", "שָלוש"),
        ("{{ 3 | מספר_מונה('ז', 'נסמך') }}", "שלושת"),
        ("{{ 1 | מספר_סודר('נ') }}", "ראשונה"),
        ("{{ 2 | מספר_סודר('ז') }}", "שני"),
        ("{{ 5 | כמות_של('ספר', 'ספרים', 'ז') }}", "חמישה ספרים"),
        ("{{ 3 | כמות_של('מחברת', 'מחברות', 'נ', מיודע=True) }}", "שְלוש מחברות"),
        ("{{ 3 | כמות_של('המחברת', 'המחברות', 'נ', מיודע='כן') }}", "שְלוש המחברות"),
        ("{{ 5 | כמות_של('ספר', 'ספרים', 'ז', מיודע='לא') }}", "חמישה ספרים"),
        ("{{ 7 | כמות('נ') }}", "שבע"),
        ("{{ 4 | כמות('ז', מיודע=True) }}", "ארבעת"),
        ("{{ 4 | כמות('ז', מיודע='כן') }}", "ארבעת"),
        ("{{ 7 | כמות('נ', מיודע='לא') }}", "שבע"),
    ],
)
def assert_jinja_render(template_str: str, expected_result: str) -> None:
    env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)
    template = env.from_string(template_str)
    result = template.render()
    assert result == expected_result
