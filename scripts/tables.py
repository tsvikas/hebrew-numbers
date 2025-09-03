"""Create a table line, used in the README file."""

from hebrew_numbers import cardinal_number, count_noun

numbers = [1, 2, 3, 22]
for n in numbers:
    print(
        n,
        count_noun(n, "ילד", "ילדים", "M", definite=False),
        count_noun(n, "הילד", "הילדים", "M", definite=True),
        count_noun(n, "ילדה", "ילדות", "F", definite=False),
        count_noun(n, "הילדה", "הילדות", "F", definite=True),
        sep=" | ",
    )
print()
for n in numbers:
    print(
        n,
        cardinal_number(n, "M", construct=False),
        cardinal_number(n, "M", construct=True),
        cardinal_number(n, "F", construct=False),
        cardinal_number(n, "F", construct=True),
        sep=" | ",
    )
