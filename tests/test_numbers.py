import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import hebrew_numbers
from hebrew_numbers import ConstructState, GrammaticalGender, InvalidNumberError

# fmt: off
NUMBERS_TO_TEST = [
    0, 1, 2, 3, 10, 11, 12, 13, 20, 21, 22, 23, 100, 101, 110, 111, 122, 200,
    222, 333, 1000, 2000, 3000, 3333, 33333, 333333, 1000000, 3333333, 33333333,
    1000000000, 3333333333,
    -1, -999, -1000000000000
]
# fmt: on


def return_errors(f, args, kwargs=None, valid_exceptions=None):
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
    data_regression: DataRegressionFixture, gender: GrammaticalGender, definite: bool
) -> None:
    data = {
        n: return_errors(
            hebrew_numbers.count_prefix,
            (n, gender),
            {"is_definite_noun": definite},
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
    data_regression: DataRegressionFixture, gender: GrammaticalGender, definite: bool
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
            {"is_definite_noun": definite},
            valid_exceptions=InvalidNumberError,
        )
        for n in NUMBERS_TO_TEST
    }
    data_regression.check(data)
