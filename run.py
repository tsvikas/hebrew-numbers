from collections.abc import Iterable
import csv

import hebrew_numbers


def maybe_str(func, i):
    try:
        return str(func(i))
    except Exception:
        return ""


def create_csv(numbers: Iterable[int]) -> str:
    number_types = [
        "indefinite_number",
        "cardinal_number_feminine",
        "cardinal_number_feminine_definite",
        "ordinal_number_feminine",
        "cardinal_number_masculine",
        "cardinal_number_masculine_definite",
        "ordinal_number_masculine",
    ]

    funcs = [getattr(hebrew_numbers, name) for name in number_types]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([""] + number_types)

    for i in numbers:
        row = [i] + [maybe_str(func, i) for func in funcs]
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
    output = create_csv(
        [
            -10,
            -3,
            *range(200),
            *range(200, 2000, 100),
            *range(2000, 20000, 1000),
            *range(20000, 100001, 10000),
            *[int(10**n) for n in range(6, 20)],
            *list(fib(200, 999999999999999)),
        ]
    )
    print(output)
