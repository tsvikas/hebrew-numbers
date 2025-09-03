from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import pytest

import hebrew_numbers
from hebrew_numbers import (
    ConstructState,
    GrammaticalGender,
    InvalidNumberError,
    cardinal_number,
)
from hebrew_numbers.hebrew_numbers import _join_words

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture


NUMBERS_TO_TEST = sorted(
    {
        -1,
        -999,
        -1_000_000_000_000,
        *range(0, 201, 1),
        *range(0, 1001, 100),
        *range(0, 20001, 1000),
        *range(0, 100001, 10000),
        *range(0, 1000001, 100000),
        *range(0, 20000001, 1000000),
        *range(0, 100000001, 10000000),
        *range(0, 2000000001, 100000000),
        *range(0, 100, 11),
        *range(0, 1000, 111),
        *range(0, 10000, 1111),
        *range(0, 100000, 11111),
        *range(0, 1000000, 111111),
        *range(0, 10000000, 1111111),
        *range(0, 100000000, 11111111),
        *range(0, 1000000000, 111111111),
        *range(0, 10000000000, 1111111111),
        *[10**n for n in range(30)],
    }
)


def return_errors(  # type: ignore[explicit-any]
    f: Callable[..., str],
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    valid_exceptions: tuple[type[Exception]] | type[Exception] | None = None,
) -> str:
    kwargs = kwargs or {}
    try:
        return f(*args, **kwargs)
    except Exception as e:
        if valid_exceptions and isinstance(e, valid_exceptions):
            return repr(e)
        raise


@pytest.mark.parametrize(
    "gender", [GrammaticalGender.FEMININE, GrammaticalGender.MASCULINE]
)
@pytest.mark.parametrize(
    "construct", [ConstructState.ABSOLUTE, ConstructState.CONSTRUCT]
)
def test_cardinal_number(
    data_regression: DataRegressionFixture,
    gender: GrammaticalGender,
    construct: ConstructState,
) -> None:
    data = {
        n: return_errors(
            hebrew_numbers.cardinal_number,
            (n, gender, construct),
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)


def test_indefinite_number(data_regression: DataRegressionFixture) -> None:
    data = {
        n: return_errors(
            hebrew_numbers.indefinite_number,
            (n,),
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)


@pytest.mark.parametrize(
    "gender", [GrammaticalGender.FEMININE, GrammaticalGender.MASCULINE]
)
def test_ordinal_number(
    data_regression: DataRegressionFixture, gender: GrammaticalGender
) -> None:
    data = {
        n: return_errors(
            hebrew_numbers.ordinal_number,
            (n, gender),
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)


@pytest.mark.parametrize(
    "gender", [GrammaticalGender.FEMININE, GrammaticalGender.MASCULINE]
)
@pytest.mark.parametrize("definite", [False, True])
def test_count_prefix(
    data_regression: DataRegressionFixture,
    gender: GrammaticalGender,
    definite: bool,  # noqa: FBT001
) -> None:
    data = {
        n: return_errors(
            hebrew_numbers.count_prefix,
            (n, gender),
            {"definite": definite},
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)


@pytest.mark.parametrize(
    "gender", [GrammaticalGender.FEMININE, GrammaticalGender.MASCULINE]
)
@pytest.mark.parametrize("definite", [False, True])
def test_count_noun(
    data_regression: DataRegressionFixture,
    gender: GrammaticalGender,
    definite: bool,  # noqa: FBT001
) -> None:
    singular_form = {
        GrammaticalGender.MASCULINE: "ילד",
        GrammaticalGender.FEMININE: "ילדה",
    }[gender]
    plural_form = {
        GrammaticalGender.MASCULINE: "ילדים",
        GrammaticalGender.FEMININE: "ילדות",
    }[gender]
    if definite:
        singular_form = "ה" + singular_form
        plural_form = "ה" + plural_form
    data = {
        n: return_errors(
            hebrew_numbers.count_noun,
            (n, singular_form, plural_form, gender),
            {"definite": definite},
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)


@pytest.mark.parametrize(
    "construct", [ConstructState.ABSOLUTE, ConstructState.CONSTRUCT]
)
def test_cardinal_number_genderless(construct: ConstructState) -> None:
    for n in NUMBERS_TO_TEST:
        nn = n * 10
        if nn % 10 == 1:
            continue
        num_f = return_errors(
            hebrew_numbers.cardinal_number,
            (nn * 10, "f", construct),
            valid_exceptions=InvalidNumberError,
        )
        num_m = return_errors(
            hebrew_numbers.cardinal_number,
            (nn * 10, "m", construct),
            valid_exceptions=InvalidNumberError,
        )
        assert num_f == num_m


@pytest.mark.parametrize(
    "gender", [GrammaticalGender.FEMININE, GrammaticalGender.MASCULINE]
)
def test_over_10(gender: GrammaticalGender) -> None:
    for n in NUMBERS_TO_TEST:
        if n <= 10:
            continue
        assert (
            return_errors(
                hebrew_numbers.cardinal_number,
                (n, gender, ConstructState.ABSOLUTE),
                valid_exceptions=InvalidNumberError,
            )
            == return_errors(
                hebrew_numbers.cardinal_number,
                (n, gender, ConstructState.CONSTRUCT),
                valid_exceptions=InvalidNumberError,
            )
            == return_errors(
                hebrew_numbers.ordinal_number,
                (n, gender),
                valid_exceptions=InvalidNumberError,
            )
        )


class TestConstructStateFromBoolean:
    """Test ConstructState.from_boolean method edge cases."""

    def test_from_boolean_with_construct_state_enum(self) -> None:
        """Test passing ConstructState enum directly returns same value."""
        # This tests the else clause in from_boolean (line 68)
        result = ConstructState.from_boolean(ConstructState.ABSOLUTE)
        assert result == ConstructState.ABSOLUTE

        result = ConstructState.from_boolean(ConstructState.CONSTRUCT)
        assert result == ConstructState.CONSTRUCT


class TestJoinWordsEdgeCases:
    """Test _join_words function with edge cases."""

    def test_join_empty_words_list(self) -> None:
        """Test that empty words list raises ValueError."""
        # This tests line 93 in hebrew_numbers.py
        with pytest.raises(
            ValueError, match="must contain at least one non-empty string"
        ):
            _join_words([])

    def test_join_only_empty_strings(self) -> None:
        """Test that list with only empty strings raises ValueError."""
        # This also tests line 93 in hebrew_numbers.py
        with pytest.raises(
            ValueError, match="must contain at least one non-empty string"
        ):
            _join_words(["", "", ""])


class TestCardinalNumberEdgeCases:
    """Test cardinal_number function with invalid inputs."""

    def test_cardinal_number_invalid_range(self) -> None:
        """Test cardinal_number with numbers outside valid range."""
        # Test zero (line 333 in hebrew_numbers.py)
        with pytest.raises(InvalidNumberError, match="Number must be positive"):
            cardinal_number(0, GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE)

        with pytest.raises(InvalidNumberError, match="Number must be positive"):
            cardinal_number(-1, GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE)
