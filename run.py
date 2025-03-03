import csv
import functools
from collections.abc import Callable, Iterable

import hebrew_numbers
from fib import fib


def maybe_str(func: Callable[[int], str], i: int) -> str:
    try:
        return str(func(i))
    except hebrew_numbers.InvalidNumberError:
        return ""


def count_female(n: int) -> str:
    return hebrew_numbers.count_noun(n, "ילדה", "ילדות", "f")


def count_female_definite(n: int) -> str:
    return hebrew_numbers.count_noun(n, "הילדה", "הילדות", "f", definite=True)


def count_male(n: int) -> str:
    return hebrew_numbers.count_noun(n, "ילד", "ילדים", "m")


def count_male_definite(n: int) -> str:
    return hebrew_numbers.count_noun(n, "הילד", "הילדים", "m", definite=True)


NUMBER_FORMS_FEMININE: dict[str, Callable[[int], str]] = {
    "indefinite_number": hebrew_numbers.indefinite_number,
    "cardinal_number_feminine_absolute": functools.partial(
        hebrew_numbers.cardinal_number, gender="f", construct=False
    ),
    "cardinal_number_feminine_construct": functools.partial(
        hebrew_numbers.cardinal_number, gender="f", construct=True
    ),
    "ordinal_number_feminine": functools.partial(
        hebrew_numbers.ordinal_number, gender="f"
    ),
    "count_female_indefinite_prefix": functools.partial(
        hebrew_numbers.count_prefix, gender="f", definite=False
    ),
    "count_female_definite_prefix": functools.partial(
        hebrew_numbers.count_prefix, gender="f", definite=True
    ),
    "count_female_indefinite_example": count_female,
    "count_female_definite_example": count_female_definite,
}
NUMBER_FORMS_MASCULINE: dict[str, Callable[[int], str]] = {
    "cardinal_number_masculine_absolute": functools.partial(
        hebrew_numbers.cardinal_number, gender="m", construct=False
    ),
    "cardinal_number_masculine_construct": functools.partial(
        hebrew_numbers.cardinal_number, gender="m", construct=True
    ),
    "ordinal_number_masculine": functools.partial(
        hebrew_numbers.ordinal_number, gender="m"
    ),
    "count_male_indefinite_prefix": functools.partial(
        hebrew_numbers.count_prefix, gender="m", definite=False
    ),
    "count_male_definite_prefix": functools.partial(
        hebrew_numbers.count_prefix, gender="m", definite=True
    ),
    "count_male_indefinite_example": count_male,
    "count_male_definite_example": count_male_definite,
}


def create_csv(numbers: Iterable[int]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "",
            "indefinite_number / cardinal_number_feminine_absolute",
            "cardinal_number_feminine_construct",
            "ordinal_number_feminine",
            "count_female_indefinite_example",
            "count_female_definite_example",
            "cardinal_number_masculine_absolute",
            "cardinal_number_masculine_construct",
            "ordinal_number_masculine",
            "count_male_indefinite_example",
            "count_male_definite_example",
        ]
    )
    for i in numbers:
        if i > 10:  # noqa: PLR2004
            f_forms = {
                maybe_str(func, i)
                for name, func in NUMBER_FORMS_FEMININE.items()
                if not name.endswith("_example")
            }
            m_forms = {
                maybe_str(func, i)
                for name, func in NUMBER_FORMS_MASCULINE.items()
                if not name.endswith("_example")
            }
            assert len(f_forms) == len(m_forms) == 1  # noqa: S101
            row = [i, *f_forms, "", "", "", "", *m_forms, "", "", "", ""]
        else:
            funcs = {
                k: v
                for k, v in NUMBER_FORMS_FEMININE.items()
                if not k.endswith("prefix")
            } | {
                k: v
                for k, v in NUMBER_FORMS_MASCULINE.items()
                if not k.endswith("prefix")
            }
            row = [i] + [maybe_str(func, i) for func in funcs.values()]
            assert i <= 0 or row[1] == row[2], f"{row[1]=}, {row[2]=}"  # noqa: S101
            del row[2]
        writer.writerow(row)
    return output.getvalue()


if __name__ == "__main__":
    import io

    max_n = 1000000000000000000000
    numbers = sorted(
        {
            -1,
            0,
            1,
            max_n - 1,
            max_n,
            -10,
            -3,
            *range(201),
            *range(0, 1001, 100),
            *range(0, 21001, 1000),
            *range(0, 100001, 10000),
            *range(0, 1000001, 100000),
            *range(0, 21000001, 1000000),
            *range(0, 21000000001, 1000000000),
            *[int(10**n) for n in range(21)],
            *[int(10**n) + 1 for n in range(21)],
            *[int(10**n) for n in range(0, 40, 3)],
            *range(0, 10_000_000_000, 1111111111),
        }
    ) + list(fib(200, max_n))
    output = create_csv(numbers)
    print(output)  # noqa: T201
