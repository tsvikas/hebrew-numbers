from collections.abc import Iterable
from pathlib import Path
import csv

import hebrew_numbers


def maybe_str(func, i):
    try:
        return str(func(i))
    except Exception:
        return ""


def create_csv(numbers: Iterable[int], output_fn: Path):
    number_types = [
        "indefinite_number",
        "cardinal_number_feminine",
        "ordinal_number_feminine",
        "cardinal_number_feminine_definite",
        "cardinal_number_masculine",
        "ordinal_number_masculine",
        "cardinal_number_masculine_definite",
    ]

    funcs = [getattr(hebrew_numbers, name) for name in number_types]

    with open(output_fn, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + number_types)

        for i in numbers:
            row = [i] + [maybe_str(func, i) for func in funcs]
            writer.writerow(row)


def fib(min: int, max: int):
    a, b = 0, 1
    while a < max:
        a, b = b, a + b
        if a > min:
            yield a


if __name__ == "__main__":
    create_csv(
        [
            -10,
            -3,
            *range(200),
            *range(200, 2000, 100),
            *range(2000, 20000, 1000),
            *range(20000, 100001, 10000),
            *[int(10**n) for n in range(6, 20)],
            *list(fib(200, 999999999999)),
        ],
        Path("output.csv"),
    )
