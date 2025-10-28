"""Jinja2 extension for Hebrew number conversion.

© 2025 Tsvika Shapira. Some rights reserved.
"""

# ruff: noqa: N803, PLC2401

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jinja2 import Environment

try:
    from jinja2.ext import Extension
except ImportError as exc:
    msg = (
        "jinja2 is required for Hebrew numbers Jinja extension. "
        "Install with: pip install hebrew-numbers[jinja]"
    )
    raise ImportError(msg) from exc

from .hebrew_numbers import (
    ConstructState,
    GrammaticalGender,
    cardinal_number,
    count_noun,
    count_prefix,
    indefinite_number,
    ordinal_number,
)

__all__ = [
    "HebrewNumbersExtension",
    "hebrew_cardinal_filter",
    "hebrew_cardinal_filter_hebrew_params",
    "hebrew_count_filter",
    "hebrew_count_filter_hebrew_params",
    "hebrew_indefinite_filter",
    "hebrew_ordinal_filter",
    "hebrew_ordinal_filter_hebrew_params",
    "hebrew_prefix_filter",
    "hebrew_prefix_filter_hebrew_params",
]


def _map_hebrew_gender(מין: str) -> GrammaticalGender:
    """Map Hebrew gender terms to English enum.

    Args:
        מין: Hebrew gender term ('ז', 'זכר', 'זכרי', 'נ', 'נקבה', 'נקבי')

    Returns:
        GrammaticalGender enum
    """
    gender_map = {
        "ז": "masculine",
        "זכר": "masculine",
        "זכרי": "masculine",
        "נ": "feminine",
        "נקבה": "feminine",
        "נקבי": "feminine",
    }

    english_gender = gender_map.get(מין, מין)
    return GrammaticalGender.from_string(english_gender)


def _map_hebrew_construct(מצב: str) -> ConstructState:
    """Map Hebrew construct state terms to English enum.

    Args:
        מצב: Hebrew construct state ('נפרד' for absolute, 'נסמך' for construct)

    Returns:
        ConstructState enum
    """
    construct_map = {
        "נפרד": "absolute",
        "נסמך": "construct",
    }

    english_construct = construct_map.get(מצב, מצב)
    return ConstructState(english_construct)


def _map_hebrew_boolean(value: bool | str) -> bool:  # noqa: FBT001
    """Map Hebrew boolean terms to Python bool.

    Args:
        value: Hebrew boolean term ('כן', 'לא') or Python bool

    Returns:
        Python boolean

    Raises:
        ValueError: If string value is not a valid Hebrew boolean term
    """
    if isinstance(value, bool):
        return value

    boolean_map = {
        "כן": True,
        "לא": False,
    }

    if value in boolean_map:
        return boolean_map[value]

    msg = (
        f"Invalid Hebrew boolean value: {value!r}. Expected 'כן', 'לא', True, or False"
    )
    raise ValueError(msg)


def hebrew_indefinite_filter(value: int) -> str:
    """Convert number to indefinite Hebrew representation.

    Args:
        value: Number to convert.

    Returns:
        Hebrew text representation.

    Example:
        >>> from jinja2 import Environment
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> env.from_string("{{ 42 | hebrew_indefinite }}").render()
        'ארבעים ושתיים'
    """
    return indefinite_number(value)


def hebrew_cardinal_filter(
    value: int,
    gender: str,
    construct: str = "absolute",
) -> str:
    """Convert number to cardinal Hebrew representation.

    Args:
        value: Number to convert.
        gender: Gender string ('m', 'male', 'masculine', 'f', 'female', 'feminine').
        construct: Either 'absolute' or 'construct'.

    Returns:
        Hebrew cardinal number.

    Example:
        >>> from jinja2 import Environment
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> template = "{{ 3 | hebrew_cardinal('feminine') }}"
        >>> env.from_string(template).render()
        'שָלוש'
    """
    gender_enum = GrammaticalGender.from_string(gender)
    construct_enum = ConstructState(construct)
    return cardinal_number(value, gender_enum, construct_enum)


def hebrew_ordinal_filter(value: int, gender: str) -> str:
    """Convert number to ordinal Hebrew representation.

    Args:
        value: Number to convert.
        gender: Gender string ('m', 'male', 'masculine', 'f', 'female', 'feminine').

    Returns:
        Hebrew ordinal number.

    Example:
        >>> from jinja2 import Environment
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> env.from_string("{{ 1 | hebrew_ordinal('feminine') }}").render()
        'ראשונה'
    """
    gender_enum = GrammaticalGender.from_string(gender)
    return ordinal_number(value, gender_enum)


def hebrew_count_filter(
    value: int,
    singular: str,
    plural: str,
    gender: str,
    *,
    definite: bool = False,
) -> str:
    """Count nouns with proper Hebrew grammar.

    Args:
        value: Number to count.
        singular: Singular form of the noun.
        plural: Plural form of the noun.
        gender: Gender string ('m', 'male', 'masculine', 'f', 'female', 'feminine').
        definite: Whether to use definite article.

    Returns:
        Hebrew text with counted noun.

    Example:
        >>> from jinja2 import Environment
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> template = "{{ 5 | hebrew_count('ספר', 'ספרים', 'masculine') }}"
        >>> env.from_string(template).render()
        'חמישה ספרים'
    """
    gender_enum = GrammaticalGender.from_string(gender)
    return count_noun(value, singular, plural, gender_enum, definite=definite)


def hebrew_prefix_filter(
    value: int,
    gender: str,
    *,
    definite: bool = False,
) -> str:
    """Get Hebrew number prefix for counting.

    Args:
        value: Number for prefix.
        gender: Gender string ('m', 'male', 'masculine', 'f', 'female', 'feminine').
        definite: Whether to use definite form.

    Returns:
        Hebrew number prefix.

    Example:
        >>> from jinja2 import Environment
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> env.from_string("{{ 7 | hebrew_prefix('feminine') }}").render()
        'שבע'
    """
    gender_enum = GrammaticalGender.from_string(gender)
    return count_prefix(value, gender_enum, definite=definite)


def hebrew_cardinal_filter_hebrew_params(
    value: int,
    מין: str,
    מצב: str = "נפרד",
) -> str:
    """Convert number to cardinal Hebrew representation (Hebrew parameter names).

    Args:
        value: Number to convert.
        מין: Gender ('ז', 'זכר', 'זכרי', 'נ', 'נקבה', 'נקבי').
        מצב: State ('נפרד' for absolute, 'נסמך' for construct).

    Returns:
        Hebrew cardinal number.
    """
    gender_enum = _map_hebrew_gender(מין)
    construct_enum = _map_hebrew_construct(מצב)
    return cardinal_number(value, gender_enum, construct_enum)


def hebrew_ordinal_filter_hebrew_params(value: int, מין: str) -> str:
    """Convert number to ordinal Hebrew representation (Hebrew parameter names).

    Args:
        value: Number to convert.
        מין: Gender ('ז', 'זכר', 'זכרי', 'נ', 'נקבה', 'נקבי').

    Returns:
        Hebrew ordinal number.
    """
    gender_enum = _map_hebrew_gender(מין)
    return ordinal_number(value, gender_enum)


def hebrew_count_filter_hebrew_params(
    value: int,
    יחיד: str,
    רבים: str,
    מין: str,
    *,
    מיודע: bool | str = False,
) -> str:
    """Count nouns with proper Hebrew grammar (Hebrew parameter names).

    Args:
        value: Number to count.
        יחיד: Singular form of the noun.
        רבים: Plural form of the noun.
        מין: Gender ('ז', 'זכר', 'זכרי', 'נ', 'נקבה', 'נקבי').
        מיודע: Whether to use definite article ('כן'/'לא' or True/False).

    Returns:
        Hebrew text with counted noun.
    """
    gender_enum = _map_hebrew_gender(מין)
    definite_bool = _map_hebrew_boolean(מיודע)
    return count_noun(value, יחיד, רבים, gender_enum, definite=definite_bool)


def hebrew_prefix_filter_hebrew_params(
    value: int,
    מין: str,
    *,
    מיודע: bool | str = False,
) -> str:
    """Get Hebrew number prefix for counting (Hebrew parameter names).

    Args:
        value: Number for prefix.
        מין: Gender ('ז', 'זכר', 'זכרי', 'נ', 'נקבה', 'נקבי').
        מיודע: Whether to use definite form ('כן'/'לא' or True/False).

    Returns:
        Hebrew number prefix.
    """
    gender_enum = _map_hebrew_gender(מין)
    definite_bool = _map_hebrew_boolean(מיודע)
    return count_prefix(value, gender_enum, definite=definite_bool)


class HebrewNumbersExtension(Extension):
    """Jinja2 extension that adds Hebrew number conversion filters.

    Provides filters for converting numbers to Hebrew text with proper
    grammatical forms including gender, definiteness, and construct state.

    Usage:
        >>> from jinja2 import Environment
        >>> from hebrew_numbers.jinja import HebrewNumbersExtension
        >>> env = Environment(extensions=[HebrewNumbersExtension])
        >>> template = env.from_string("{{ 42 | hebrew_indefinite }}")
        >>> template.render()
        'ארבעים ושתיים'
    """

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension and register filters.

        Args:
            environment: The Jinja2 environment to extend.
        """
        super().__init__(environment)
        # English filter names
        environment.filters["hebrew_indefinite"] = hebrew_indefinite_filter
        environment.filters["hebrew_cardinal"] = hebrew_cardinal_filter
        environment.filters["hebrew_ordinal"] = hebrew_ordinal_filter
        environment.filters["hebrew_count"] = hebrew_count_filter
        environment.filters["hebrew_prefix"] = hebrew_prefix_filter

        # Hebrew filter names with Hebrew parameters
        environment.filters["מספר_סתמי"] = hebrew_indefinite_filter
        environment.filters["מספר_מונה"] = hebrew_cardinal_filter_hebrew_params
        environment.filters["מספר_סודר"] = hebrew_ordinal_filter_hebrew_params
        environment.filters["כמות_של"] = hebrew_count_filter_hebrew_params
        environment.filters["כמות"] = hebrew_prefix_filter_hebrew_params
