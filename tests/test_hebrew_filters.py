"""Test script for Hebrew-named Jinja filters."""

from jinja2 import Environment

from hebrew_numbers.jinja import HebrewNumbersExtension


def test_hebrew_filters() -> None:
    """Test all Hebrew-named filters."""
    env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

    # Test מספר_סתמי (indefinite number)
    template = env.from_string("{{ 5 | מספר_סתמי }}")
    result = template.render()
    assert result == "חמש"

    # Test מספר_מונה (cardinal number with Hebrew params)
    template = env.from_string("{{ 3 | מספר_מונה('נ', 'נפרד') }}")
    result = template.render()
    assert result == "שָלוש"

    template = env.from_string("{{ 3 | מספר_מונה('ז', 'נסמך') }}")
    result = template.render()
    assert result == "שלושת"

    # Test מספר_סודר (ordinal number with Hebrew params)
    template = env.from_string("{{ 1 | מספר_סודר('נ') }}")
    result = template.render()
    assert result == "ראשונה"

    template = env.from_string("{{ 2 | מספר_סודר('ז') }}")
    result = template.render()
    assert result == "שני"

    # Test כמות_של (count nouns with Hebrew params)
    template = env.from_string("{{ 5 | כמות_של('ספר', 'ספרים', 'ז') }}")
    result = template.render()
    assert result == "חמישה ספרים"

    template = env.from_string("{{ 3 | כמות_של('מחברת', 'מחברות', 'נ', מיודע=True) }}")
    result = template.render()
    assert result == "שְלוש מחברות"

    # Test Hebrew boolean values for מיודע
    template = env.from_string(
        "{{ 3 | כמות_של('המחברת', 'המחברות', 'נ', מיודע='כן') }}"
    )
    result = template.render()
    assert result == "שְלוש המחברות"

    template = env.from_string("{{ 5 | כמות_של('ספר', 'ספרים', 'ז', מיודע='לא') }}")
    result = template.render()
    assert result == "חמישה ספרים"

    # Test כמות (prefix with Hebrew params)
    template = env.from_string("{{ 7 | כמות('נ') }}")
    result = template.render()
    assert result == "שבע"

    template = env.from_string("{{ 4 | כמות('ז', מיודע=True) }}")
    result = template.render()
    assert result == "ארבעת"

    # Test Hebrew boolean values for כמות
    template = env.from_string("{{ 4 | כמות('ז', מיודע='כן') }}")
    result = template.render()
    assert result == "ארבעת"

    template = env.from_string("{{ 7 | כמות('נ', מיודע='לא') }}")
    result = template.render()
    assert result == "שבע"


if __name__ == "__main__":
    test_hebrew_filters()
