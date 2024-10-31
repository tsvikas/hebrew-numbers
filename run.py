from collections.abc import Iterable
import csv

import hebrew_numbers


def maybe_str(func, i):
    try:
        return str(func(i))
    except Exception:
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
        "cardinal_number_feminine": hebrew_numbers.cardinal_number_feminine,
        "cardinal_number_feminine_definite": hebrew_numbers.cardinal_number_feminine_definite,
        "ordinal_number_feminine": hebrew_numbers.ordinal_number_feminine,
        "cardinal_number_masculine": hebrew_numbers.cardinal_number_masculine,
        "cardinal_number_masculine_definite": hebrew_numbers.cardinal_number_masculine_definite,
        "ordinal_number_masculine": hebrew_numbers.ordinal_number_masculine,
        "count_female": count_female,
        "count_female_definite": count_female_definite,
        "count_male": count_male,
        "count_male_definite": count_male_definite,
    }
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([""] + list(funcs))

    for i in numbers:
        row = [i] + [maybe_str(func, i) for func in funcs.values()]
        writer.writerow(row)
    return output.getvalue()


def fib(min: int, max: int):
    a, b = 0, 1
    while b < max:
        a, b = b, a + b
        if a > min:
            yield a


if __name__ == "__main__":
    import io

    numbers = sorted(
        {
            -1,
            0,
            1,
            1000000000000000 - 1,
            -10,
            -3,
            *range(200),
            *range(0, 2000, 100),
            *range(0, 20000, 1000),
            *range(0, 100001, 10000),
            *[int(10**n) for n in range(0, 20)],
            *[int(10**n) + 1 for n in range(0, 20)],
            *list(fib(1, 999999999999999)),
        }
    )
    output = create_csv(numbers)
    print(output)
