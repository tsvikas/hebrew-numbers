"""Create numbers for fibbonaci numbers."""

from collections.abc import Generator

import hebrew_numbers


def fib(min: int, max: int) -> Generator[int]:  # noqa: A002
    """Create fibonacci numbers."""
    a, b = 1, 1
    while b < max:
        a, b = b, a + b
        if a > min:
            yield a


def main() -> None:
    """Print fibbonacci numbers in Hebrew."""
    for n in fib(0, 1_000_000_000_000_000_000_000):
        print(hebrew_numbers.indefinite_number(n))


if __name__ == "__main__":
    main()
