import csv
import functools
from collections.abc import Iterable

import hebrew_numbers


def maybe_str(func, i):
    try:
        return str(func(i))
    except hebrew_numbers.InvalidNumberError:
        return ""


def count_female(n: int) -> str:
    return hebrew_numbers.count_noun(
        n, "ילדה", "ילדות", hebrew_numbers.GrammaticalGender.FEMININE
    )


def count_female_definite(n: int) -> str:
    return hebrew_numbers.count_noun(
        n,
        "הילדה",
        "הילדות",
        hebrew_numbers.GrammaticalGender.FEMININE,
        is_definite_noun=True,
    )


def count_male(n: int) -> str:
    return hebrew_numbers.count_noun(
        n, "ילד", "ילדים", hebrew_numbers.GrammaticalGender.MASCULINE
    )


def count_male_definite(n: int) -> str:
    return hebrew_numbers.count_noun(
        n,
        "הילד",
        "הילדים",
        hebrew_numbers.GrammaticalGender.MASCULINE,
        is_definite_noun=True,
    )


def create_csv(numbers: Iterable[int]) -> str:
    funcs = {
        "indefinite_number": hebrew_numbers.indefinite_number,
        "cardinal_number_feminine": functools.partial(
            hebrew_numbers.count_prefix, gender="f", is_definite_noun=False
        ),
        "cardinal_number_feminine_definite": functools.partial(
            hebrew_numbers.count_prefix, gender="f", is_definite_noun=True
        ),
        "ordinal_number_feminine": functools.partial(
            hebrew_numbers.ordinal_number, gender="f"
        ),
        "cardinal_number_masculine": functools.partial(
            hebrew_numbers.count_prefix, gender="m", is_definite_noun=False
        ),
        "cardinal_number_masculine_definite": functools.partial(
            hebrew_numbers.count_prefix, gender="m", is_definite_noun=True
        ),
        "ordinal_number_masculine": functools.partial(
            hebrew_numbers.ordinal_number, gender="m"
        ),
        "count_female": count_female,
        "count_female_definite": count_female_definite,
        "count_male": count_male,
        "count_male_definite": count_male_definite,
    }
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["", *funcs])
    writer.writerow(
        ["סוג"]
        + [
            (
                "סתמי"
                if name.startswith("indefinite")
                else (
                    "מונה"
                    if name.startswith("cardinal")
                    else (
                        "סודר"
                        if name.startswith("ordinal")
                        else "דוגמת שימוש" if name.startswith("count") else ""
                    )
                )
            )
            for name in funcs
        ]
    )
    writer.writerow(
        ["מין"]
        + [
            "נקבה" if "feminine" in name else "זכר" if "masculine" in name else ""
            for name in funcs
        ]
    )
    writer.writerow(
        ["נסמך/מיודע"] + ["כן" if "_definite" in name else "" for name in funcs]
    )

    for i in numbers:
        row = [i] + [maybe_str(func, i) for func in funcs.values()]
        writer.writerow(row)
    return output.getvalue()


def fib(min: int, max: int):  # noqa: A002
    a, b = 0, 1
    while b < max:
        a, b = b, a + b
        if a > min:
            yield a


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
            *range(301),
            *range(0, 2001, 100),
            *range(0, 30001, 1000),
            *range(0, 200001, 10000),
            *range(0, 2000001, 100000),
            *range(0, 30000001, 1000000),
            *range(0, 30000000001, 1000000000),
            *[int(10**n) for n in range(20)],
            *[int(10**n) + 1 for n in range(20)],
            *[int(10**n) for n in range(0, 40, 3)],
            *list(fib(1, max_n)),
        }
    )
    output = create_csv(numbers)
    print(output)  # noqa: T201
