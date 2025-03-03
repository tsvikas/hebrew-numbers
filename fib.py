from collections.abc import Generator

import hebrew_numbers


def fib(min: int, max: int) -> Generator[int]:  # noqa: A002
    a, b = 1, 1
    while b < max:
        a, b = b, a + b
        if a > min:
            yield a


def main() -> None:
    for n in fib(0, 1_000_000_000_000_000_000_000):
        print(hebrew_numbers.indefinite_number(n))  # noqa: T201


if __name__ == "__main__":
    main()
