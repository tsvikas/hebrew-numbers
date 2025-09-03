"""Tests for Jinja2 extension."""

from __future__ import annotations

import pytest

pytest.importorskip("jinja2")

from jinja2 import Environment

from hebrew_numbers import InvalidNumberError
from hebrew_numbers.jinja import (
    HebrewNumbersExtension,
    hebrew_cardinal_filter,
    hebrew_count_filter,
    hebrew_indefinite_filter,
    hebrew_ordinal_filter,
    hebrew_prefix_filter,
)


class TestHebrewNumbersExtension:
    """Test the Jinja2 extension registration and functionality."""

    def test_extension_registration(self) -> None:
        """Test that extension registers filters correctly."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        expected_filters = {
            "hebrew_indefinite",
            "hebrew_cardinal",
            "hebrew_ordinal",
            "hebrew_count",
            "hebrew_prefix",
        }

        for filter_name in expected_filters:
            assert filter_name in env.filters

    def test_hebrew_indefinite_filter_integration(self) -> None:
        """Test hebrew_indefinite filter through template rendering."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)
        template = env.from_string("{{ 42 | hebrew_indefinite }}")
        result = template.render()
        assert result == "ארבעים ושתיים"

    def test_hebrew_cardinal_filter_integration(self) -> None:
        """Test hebrew_cardinal filter through template rendering."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        # Test with masculine gender
        template = env.from_string("{{ 3 | hebrew_cardinal('masculine') }}")
        result = template.render()
        assert result == "שלושה"

        # Test with feminine gender
        template = env.from_string("{{ 3 | hebrew_cardinal('feminine') }}")
        result = template.render()
        assert result == "שָלוש"

        # Test with construct state
        template = env.from_string(
            "{{ 3 | hebrew_cardinal('masculine', 'construct') }}"
        )
        result = template.render()
        assert result == "שלושת"

    def test_hebrew_ordinal_filter_integration(self) -> None:
        """Test hebrew_ordinal filter through template rendering."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        # Test masculine
        template = env.from_string("{{ 1 | hebrew_ordinal('masculine') }}")
        result = template.render()
        assert result == "ראשון"

        # Test feminine
        template = env.from_string("{{ 1 | hebrew_ordinal('feminine') }}")
        result = template.render()
        assert result == "ראשונה"

    def test_hebrew_count_filter_integration(self) -> None:
        """Test hebrew_count filter through template rendering."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template = env.from_string(
            "{{ 5 | hebrew_count('ספר', 'ספרים', 'masculine') }}"
        )
        result = template.render()
        assert result == "חמישה ספרים"

        # Test with definite article
        template = env.from_string(
            "{{ 5 | hebrew_count('הספר', 'הספרים', 'masculine', definite=true) }}"
        )
        result = template.render()
        assert result == "חמשת הספרים"

    def test_hebrew_prefix_filter_integration(self) -> None:
        """Test hebrew_prefix filter through template rendering."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        # Test masculine
        template = env.from_string("{{ 7 | hebrew_prefix('masculine') }}")
        result = template.render()
        assert result == "שבעה"

        # Test feminine
        template = env.from_string("{{ 7 | hebrew_prefix('feminine') }}")
        result = template.render()
        assert result == "שבע"

    def test_complex_template(self) -> None:
        """Test using multiple filters in a single template."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template_str = """
        Indefinite: {{ 42 | hebrew_indefinite }}
        Cardinal: {{ 3 | hebrew_cardinal('feminine') }}
        Ordinal: {{ 1 | hebrew_ordinal('masculine') }}
        Count: {{ 5 | hebrew_count('ספר', 'ספרים', 'masculine') }}
        Prefix: {{ 7 | hebrew_prefix('feminine') }}
        """

        template = env.from_string(template_str)
        result = template.render()

        assert "ארבעים ושתיים" in result
        assert "שָלוש" in result
        assert "ראשון" in result
        assert "חמישה ספרים" in result
        assert "שבע" in result


class TestIndividualFilters:
    """Test individual filter functions directly."""

    def test_hebrew_indefinite_filter(self) -> None:
        """Test hebrew_indefinite_filter function."""
        assert hebrew_indefinite_filter(42) == "ארבעים ושתיים"
        assert hebrew_indefinite_filter(1) == "אחת"

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
        result = hebrew_indefinite_filter(-1)
        assert "מינוס" in result

        # Invalid gender raises ValueError
        with pytest.raises(ValueError, match="Invalid gender"):
            hebrew_cardinal_filter(1, "invalid_gender")

        with pytest.raises(InvalidNumberError):
            hebrew_ordinal_filter(0, "masculine")


class TestTemplateEdgeCases:
    """Test edge cases and error conditions in templates."""

    def test_template_with_zero(self) -> None:
        """Test templates with zero values."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template = env.from_string("{{ 0 | hebrew_indefinite }}")
        result = template.render()
        assert result == "אפס"

    def test_template_with_large_numbers(self) -> None:
        """Test templates with large numbers."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template = env.from_string("{{ 1000 | hebrew_indefinite }}")
        result = template.render()
        assert result == "אלף"

    def test_template_variable_substitution(self) -> None:
        """Test using template variables with filters."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template = env.from_string("{{ num | hebrew_cardinal(gender) }}")
        result = template.render(num=3, gender="feminine")
        assert result == "שָלוש"

    def test_filter_chaining(self) -> None:
        """Test that Hebrew filters can be chained with built-in filters."""
        env = Environment(extensions=[HebrewNumbersExtension], autoescape=True)

        template = env.from_string("{{ 42 | hebrew_indefinite | upper }}")
        result = template.render()
        assert result == "ארבעים ושתיים"  # Hebrew text doesn't change with upper()
