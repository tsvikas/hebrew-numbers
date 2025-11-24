"""Tests for Jinja2 extension."""

from __future__ import annotations

import pytest

pytest.importorskip("jinja2")

from jinja2 import Environment

from hebrew_numbers import InvalidNumberError
from hebrew_numbers.jinja import (
    HebrewNumbersExtension,
    _map_hebrew_boolean,
    hebrew_cardinal_filter,
    hebrew_cardinal_filter_hebrew_params,
    hebrew_count_filter,
    hebrew_count_filter_hebrew_params,
    hebrew_indefinite_filter,
    hebrew_ordinal_filter,
    hebrew_ordinal_filter_hebrew_params,
    hebrew_prefix_filter,
    hebrew_prefix_filter_hebrew_params,
)


@pytest.mark.parametrize(
    ("template_str", "expected_result"),
    [
        ("{{ 42 | hebrew_indefinite }}", "ארבעים ושתיים"),
        ("{{ 3 | hebrew_cardinal('masculine') }}", "שלושה"),
        ("{{ 3 | hebrew_cardinal('feminine') }}", "שָלוש"),
        ("{{ 3 | hebrew_cardinal('masculine', 'construct') }}", "שלושת"),
        ("{{ 1 | hebrew_ordinal('masculine') }}", "ראשון"),
        ("{{ 1 | hebrew_ordinal('feminine') }}", "ראשונה"),
        ("{{ 5 | hebrew_count('ספר', 'ספרים', 'masculine') }}", "חמישה ספרים"),
        (
            "{{ 5 | hebrew_count('הספר', 'הספרים', 'masculine', definite=true) }}",
            "חמשת הספרים",
        ),
        ("{{ 7 | hebrew_prefix('masculine') }}", "שבעה"),
        ("{{ 7 | hebrew_prefix('feminine') }}", "שבע"),
        ("{{ 0 | hebrew_indefinite }}", "אפס"),
        ("{{ 1000 | hebrew_indefinite }}", "אלף"),
    ],
)
def assert_jinja_render(template_str: str, expected_result: str) -> None:
    env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)
    template = env.from_string(template_str)
    result = template.render()
    assert result == expected_result


class TestIndividualFilters:
    """Test individual filter functions directly."""

    def test_hebrew_indefinite_filter(self) -> None:
        """Test hebrew_indefinite_filter function."""
        assert hebrew_indefinite_filter(42) == "ארבעים ושתיים"
        assert hebrew_indefinite_filter(1) == "אחת"
        assert "מינוס" in hebrew_indefinite_filter(-1)

    def test_hebrew_cardinal_filter(self) -> None:
        """Test hebrew_cardinal_filter function."""
        # Test masculine
        assert hebrew_cardinal_filter(3, "masculine") == "שלושה"

        # Test feminine
        assert hebrew_cardinal_filter(3, "feminine") == "שָלוש"

        # Test construct
        assert hebrew_cardinal_filter(3, "masculine", "construct") == "שלושת"
        assert hebrew_cardinal_filter(3, "feminine", "construct") == "שְלוש"

        # Test short gender formats
        assert hebrew_cardinal_filter(3, "m") == "שלושה"
        assert hebrew_cardinal_filter(3, "f") == "שָלוש"
        assert hebrew_cardinal_filter(3, "male") == "שלושה"
        assert hebrew_cardinal_filter(3, "female") == "שָלוש"

    def test_hebrew_ordinal_filter(self) -> None:
        """Test hebrew_ordinal_filter function."""
        # Test masculine
        assert hebrew_ordinal_filter(1, "masculine") == "ראשון"
        assert hebrew_ordinal_filter(2, "masculine") == "שני"

        # Test feminine
        assert hebrew_ordinal_filter(1, "feminine") == "ראשונה"
        assert hebrew_ordinal_filter(2, "feminine") == "שנייה"

        # Test short gender formats
        assert hebrew_ordinal_filter(1, "m") == "ראשון"
        assert hebrew_ordinal_filter(1, "f") == "ראשונה"

    def test_hebrew_count_filter(self) -> None:
        """Test hebrew_count_filter function."""
        # Test basic counting
        result = hebrew_count_filter(5, "ספר", "ספרים", "masculine", definite=False)
        assert result == "חמישה ספרים"

        # Test with definite article
        result = hebrew_count_filter(5, "הספר", "הספרים", "masculine", definite=True)
        assert result == "חמשת הספרים"

        # Test feminine
        result = hebrew_count_filter(3, "בחורה", "בחורות", "feminine", definite=False)
        assert result == "שָלוש בחורות"

        # Test short gender formats
        result = hebrew_count_filter(2, "ספר", "ספרים", "m", definite=False)
        assert result == "שני ספרים"
        result = hebrew_count_filter(3, "בחורה", "בחורות", "f", definite=False)
        assert result == "שָלוש בחורות"

    def test_hebrew_prefix_filter(self) -> None:
        """Test hebrew_prefix_filter function."""
        # Test masculine
        assert hebrew_prefix_filter(7, "masculine") == "שבעה"

        # Test feminine
        assert hebrew_prefix_filter(7, "feminine") == "שבע"

        # Test short gender formats
        assert hebrew_prefix_filter(7, "m") == "שבעה"
        assert hebrew_prefix_filter(7, "f") == "שבע"

        # Test definite
        assert hebrew_prefix_filter(7, "masculine", definite=True) == "שבעת"

    def test_filter_error_handling(self) -> None:
        """Test that filters handle invalid input appropriately."""
        # Negative numbers don't raise errors, they return "מינוס" + number

        # Invalid gender raises ValueError
        with pytest.raises(ValueError, match="Invalid gender"):
            hebrew_cardinal_filter(1, "invalid_gender")

        with pytest.raises(InvalidNumberError):
            hebrew_ordinal_filter(0, "masculine")


@pytest.mark.parametrize(
    ("n", "gender", "expected"),
    [
        (3, "ז", "שלושה"),
        (3, "זכר", "שלושה"),
        (3, "זכרי", "שלושה"),
        (3, "נ", "שָלוש"),
        (3, "נקבה", "שָלוש"),
        (3, "נקבי", "שָלוש"),
    ],
)
def test_hebrew_cardinal_filter_hebrew_params_gender(
    n: int, gender: str, expected: str
) -> None:
    """Test hebrew_cardinal_filter_hebrew_params with various Hebrew gender terms."""
    assert hebrew_cardinal_filter_hebrew_params(n, gender) == expected


@pytest.mark.parametrize(
    ("n", "gender", "construct", "expected"),
    [
        (3, "ז", "נסמך", "שלושת"),
        (3, "נ", "נסמך", "שְלוש"),
        (3, "ז", "נפרד", "שלושה"),
    ],
)
def test_hebrew_cardinal_filter_hebrew_params_construct(
    n: int, gender: str, construct: str, expected: str
) -> None:
    """Test hebrew_cardinal_filter_hebrew_params with Hebrew construct state terms."""
    assert hebrew_cardinal_filter_hebrew_params(n, gender, construct) == expected


@pytest.mark.parametrize(
    ("n", "gender", "expected"),
    [
        (1, "ז", "ראשון"),
        (2, "זכר", "שני"),
        (3, "זכרי", "שלישי"),
        (1, "נ", "ראשונה"),
        (2, "נקבה", "שנייה"),
        (3, "נקבי", "שלישית"),
    ],
)
def test_hebrew_ordinal_filter_hebrew_params(
    n: int, gender: str, expected: str
) -> None:
    """Test hebrew_ordinal_filter_hebrew_params with Hebrew gender terms."""
    assert hebrew_ordinal_filter_hebrew_params(n, gender) == expected


@pytest.mark.parametrize(
    ("n", "singular", "plural", "gender", "definite", "expected"),
    [
        (5, "ספר", "ספרים", "ז", "לא", "חמישה ספרים"),
        (5, "הספר", "הספרים", "ז", "כן", "חמשת הספרים"),
        (3, "בחורה", "בחורות", "נ", False, "שָלוש בחורות"),
        (3, "הבחורה", "הבחורות", "נ", True, "שְלוש הבחורות"),
    ],
)
def test_hebrew_count_filter_hebrew_params(  # noqa: PLR0913
    n: int,
    singular: str,
    plural: str,
    gender: str,
    definite: bool | str,  # noqa: FBT001
    expected: str,
) -> None:
    """Test hebrew_count_filter_hebrew_params with Hebrew boolean terms."""
    result = hebrew_count_filter_hebrew_params(
        n, singular, plural, gender, מיודע=definite
    )
    assert result == expected


@pytest.mark.parametrize(
    ("n", "gender", "definite", "expected"),
    [
        (7, "ז", None, "שבעה"),
        (7, "נ", None, "שבע"),
        (7, "ז", "כן", "שבעת"),
        (7, "ז", "לא", "שבעה"),
        (7, "ז", True, "שבעת"),
        (7, "ז", False, "שבעה"),
    ],
)
def test_hebrew_prefix_filter_hebrew_params(
    n: int, gender: str, definite: bool | str | None, expected: str  # noqa: FBT001
) -> None:
    """Test hebrew_prefix_filter_hebrew_params with Hebrew parameters."""
    if definite is None:
        result = hebrew_prefix_filter_hebrew_params(n, gender)
    else:
        result = hebrew_prefix_filter_hebrew_params(n, gender, מיודע=definite)
    assert result == expected


def test_map_hebrew_boolean_invalid() -> None:
    """Test _map_hebrew_boolean with invalid Hebrew boolean value."""
    with pytest.raises(ValueError, match="Invalid Hebrew boolean value"):
        _map_hebrew_boolean("invalid")


@pytest.mark.parametrize(
    ("template_str", "expected_result"),
    [
        ("{{ 42 | מספר_סתמי }}", "ארבעים ושתיים"),
        ("{{ 3 | מספר_מונה('ז') }}", "שלושה"),
        ("{{ 3 | מספר_מונה('נ', 'נסמך') }}", "שְלוש"),
        ("{{ 1 | מספר_סודר('ז') }}", "ראשון"),
        ("{{ 1 | מספר_סודר('נ') }}", "ראשונה"),
        ("{{ 5 | כמות_של('ספר', 'ספרים', 'ז') }}", "חמישה ספרים"),
        ("{{ 7 | כמות('ז') }}", "שבעה"),
    ],
)
def test_hebrew_filter_names_in_jinja(template_str: str, expected_result: str) -> None:
    """Test using Hebrew filter names in Jinja templates."""
    env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)
    template = env.from_string(template_str)
    assert template.render() == expected_result
