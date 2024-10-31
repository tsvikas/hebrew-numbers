import enum
import functools


class GrammaticalGender(enum.Enum):
    FEMININE = 0  # צורת נקבה
    MASCULINE = 1  # צורת זכר


class ConstructState(enum.Enum):
    ABSOLUTE = 0  # צורת נפרד
    CONSTRUCT = 1  # צורת נסמך


def join_words(
    words: list[str], sep: str = " ", last_sep: str = " ו"  # noqa: RUF001
) -> str:
    words = [w for w in words if w]
    if not words:
        raise ValueError("words must be non-empty")
    if len(words) == 1:
        return words[0]
    return f"{sep.join(words[:-1])}{last_sep}{words[-1]}"


def translate_one_digit(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> str:
    if not 1 <= n <= 9:  # noqa: PLR2004
        raise ValueError("number needs to be between 1 to 9")
    match grammatical_gender:
        case GrammaticalGender.FEMININE:
            match construct_state:
                case ConstructState.ABSOLUTE:
                    return {
                        1: "אחת",
                        2: "שתיים",
                        3: "שָלוש",
                        4: "ארבע",
                        5: "חמש",
                        6: "שש",
                        7: "שבע",
                        8: "שמונֶה",
                        9: "תשע",
                    }[n]
                case ConstructState.CONSTRUCT:
                    return {
                        1: "אחת",
                        2: "שתי",
                        3: "שְלוש",
                        4: "ארבע",
                        5: "חמש",
                        6: "שש",
                        7: "שבע",
                        8: "שמונֶה",
                        9: "תשע",
                    }[n]

        case GrammaticalGender.MASCULINE:
            match construct_state:
                case ConstructState.ABSOLUTE:
                    return {
                        1: "אֶחָד",
                        2: "שניים",
                        3: "שלושה",
                        4: "ארבעה",
                        5: "חמישה",
                        6: "שישה",
                        7: "שבעה",
                        8: "שמונָה",
                        9: "תשעה",
                    }[n]
                case ConstructState.CONSTRUCT:
                    return {
                        1: "אַחַד",
                        2: "שני",
                        3: "שלושת",
                        4: "ארבעת",
                        5: "חמשת",
                        6: "ששת",
                        7: "שבעת",
                        8: "שמונת",
                        9: "תשעת",
                    }[n]
    raise ValueError("invalid values")


def translate_to_20(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> str:
    if not 1 <= n <= 19:  # noqa: PLR2004
        raise ValueError("number needs to be between 1 to 19")
    if n < 10:  # noqa: PLR2004
        return translate_one_digit(n, grammatical_gender, construct_state)
    if n == 10:  # noqa: PLR2004
        return {
            (GrammaticalGender.FEMININE, ConstructState.ABSOLUTE): "עשר",
            (GrammaticalGender.FEMININE, ConstructState.CONSTRUCT): "עשר",
            (GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE): "עשרה",
            (GrammaticalGender.MASCULINE, ConstructState.CONSTRUCT): "עשרת",
        }[grammatical_gender, construct_state]
    if n == 11:  # noqa: PLR2004
        n_str = translate_one_digit(
            n % 10, grammatical_gender, ConstructState.CONSTRUCT
        )
    elif n == 12:  # noqa: PLR2004
        n_str = {
            GrammaticalGender.FEMININE: "שתים",
            GrammaticalGender.MASCULINE: "שנים",
        }[grammatical_gender]
    else:
        n_str = translate_one_digit(
            n % 10,
            grammatical_gender,
            {
                GrammaticalGender.FEMININE: ConstructState.CONSTRUCT,
                GrammaticalGender.MASCULINE: ConstructState.ABSOLUTE,
            }[grammatical_gender],
        )
    suffix = {GrammaticalGender.FEMININE: "־עשרה", GrammaticalGender.MASCULINE: "־עשר"}[
        grammatical_gender
    ]
    return f"{n_str}{suffix}"


def decompose_hundreds(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> list[str]:
    if not 1 <= n <= 999:  # noqa: PLR2004
        raise ValueError("number needs to be between 1 to 999")
    hundreds_digit = n // 100
    if hundreds_digit == 0:
        hundreds_word = ""
    elif hundreds_digit == 1:
        hundreds_word = "מאה"
    elif hundreds_digit == 2:  # noqa: PLR2004
        hundreds_word = "מאתיים"
    else:
        hundreds_word = (
            translate_one_digit(
                hundreds_digit, GrammaticalGender.FEMININE, ConstructState.CONSTRUCT
            )
            + " מאות"
        )

    tenth_digit = n % 100 // 10
    if tenth_digit > 1:
        tenth_word = {
            2: "עשרים",
            3: "שלושים",
            4: "ארבעים",
            5: "חמישים",
            6: "שישים",
            7: "שבעים",
            8: "שמונים",
            9: "תשעים",
        }[tenth_digit]
        last_digits = n % 100 - tenth_digit * 10
    else:
        tenth_word = ""
        last_digits = n % 100
        assert last_digits < 20  # noqa: PLR2004, S101

    if last_digits:
        last_digits_word = translate_to_20(
            last_digits,
            grammatical_gender,
            ConstructState.ABSOLUTE if n >= 20 else construct_state,  # noqa: PLR2004
        )
    else:

        last_digits_word = ""

    return [hundreds_word, tenth_word, last_digits_word]


def number(  # noqa: C901
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> str:
    if n >= 1_000_000_000_000_000:  # noqa: PLR2004
        raise NotImplementedError("Number is too large")
    if n < 0:
        raise ValueError("Negative number")
    if n == 0:
        if construct_state == ConstructState.CONSTRUCT:
            raise ValueError("Construct can't be zero")
        return "אפס"

    def add_suffix(n: int, suffix: str, grammatical_gender: GrammaticalGender) -> str:
        if n == 0:
            return ""
        if n == 1:
            return suffix
        n_str = join_words(
            decompose_hundreds(n, grammatical_gender, ConstructState.ABSOLUTE)
        )
        return f"{n_str} {suffix}"

    trillions = n // 1_000_000_000_000
    trillions_word = add_suffix(trillions, "טריליון", GrammaticalGender.MASCULINE)

    billions = n % 1_000_000_000_000 // 1_000_000_000
    billions_word = add_suffix(billions, "מיליארד", GrammaticalGender.MASCULINE)

    millions = n % 1_000_000_000 // 1_000_000
    millions_word = add_suffix(millions, "מיליון", GrammaticalGender.MASCULINE)

    thousands = n % 1_000_000 // 1_000
    if thousands == 0:
        thousands_word = ""
    elif thousands == 1:
        thousands_word = "אלף"
    elif thousands == 2:  # noqa: PLR2004
        thousands_word = "אלפיים"
    elif thousands <= 10:  # noqa: PLR2004
        thousands_word = (
            join_words(
                decompose_hundreds(
                    thousands, GrammaticalGender.MASCULINE, ConstructState.CONSTRUCT
                )
            )
            + " אלפים"
        )
    else:
        thousands_word = (
            join_words(
                decompose_hundreds(
                    thousands, GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE
                )
            )
            + " אלף"
        )

    last_digits = n % 1_000
    if last_digits == 0:
        last_digits_words = []
    else:
        last_digits_words = decompose_hundreds(
            last_digits,
            grammatical_gender,
            construct_state if n < 1000 else ConstructState.ABSOLUTE,  # noqa: PLR2004
        )

    words = [
        trillions_word,
        billions_word,
        millions_word,
        thousands_word,
        *last_digits_words,
    ]
    return join_words(words)


# מספר מונה
def cardinal_number(
    n: int, grammatical_gender: GrammaticalGender, *, is_definite_noun: bool = False
) -> str:
    if n < 0:
        raise ValueError("must use a non-negative number")
    if n == 1:
        return number(n, grammatical_gender, ConstructState.CONSTRUCT if is_definite_noun else ConstructState.ABSOLUTE)
    if 2 <= n <= (10 if is_definite_noun else 2):  # noqa: PLR2004
        return number(n, grammatical_gender, ConstructState.CONSTRUCT)
    return number(n, grammatical_gender, ConstructState.ABSOLUTE)


def count_noun(
    n: int,
    singular_form: str,
    plural_form: str,
    grammatical_gender: GrammaticalGender,
    *,
    is_definite_noun: bool = False,
) -> str:
    n_str = cardinal_number(n, grammatical_gender, is_definite_noun=is_definite_noun and n != 1)
    if n == 1:
        return f"{singular_form} {'ה' if is_definite_noun else ''}{n_str}"
    return f"{n_str} {plural_form}"


# מספר סתמי
def indefinite_number(n: int) -> str:
    if n < 0:
        n_str = number(-n, GrammaticalGender.FEMININE, ConstructState.ABSOLUTE)
        return f"מינוס {n_str}"
    return number(n, GrammaticalGender.FEMININE, ConstructState.ABSOLUTE)


# מספר סודר
def ordinal_number(n: int, grammatical_gender: GrammaticalGender) -> str:
    if n <= 0:
        raise ValueError("Ordinal numbers are only defined for positive integers")
    if n > 10:  # noqa: PLR2004
        return number(n, grammatical_gender, ConstructState.ABSOLUTE)
    if grammatical_gender == GrammaticalGender.FEMININE:
        return {
            1: "ראשונה",
            2: "שנייה",
            3: "שלישית",
            4: "רביעית",
            5: "חמישית",
            6: "שישית",
            7: "שביעית",
            8: "שמינית",
            9: "תשיעית",
            10: "עשירית",
        }[n]
    if grammatical_gender == GrammaticalGender.MASCULINE:
        return {
            1: "ראשון",
            2: "שני",
            3: "שלישי",
            4: "רביעי",
            5: "חמישי",
            6: "שישי",
            7: "שביעי",
            8: "שמיני",
            9: "תשיעי",
            10: "עשירי",
        }[n]
    raise ValueError("Invalid grammatical state")


ordinal_number_masculine = functools.partial(
    ordinal_number, grammatical_gender=GrammaticalGender.MASCULINE
)
ordinal_number_feminine = functools.partial(
    ordinal_number, grammatical_gender=GrammaticalGender.FEMININE
)
cardinal_number_masculine = functools.partial(
    cardinal_number, grammatical_gender=GrammaticalGender.MASCULINE
)
cardinal_number_feminine = functools.partial(
    cardinal_number, grammatical_gender=GrammaticalGender.FEMININE
)
cardinal_number_masculine_definite = functools.partial(
    cardinal_number,
    grammatical_gender=GrammaticalGender.MASCULINE,
    is_definite_noun=True,
)
cardinal_number_feminine_definite = functools.partial(
    cardinal_number,
    grammatical_gender=GrammaticalGender.FEMININE,
    is_definite_noun=True,
)
count_noun_masculine = functools.partial(
    count_noun, grammatical_gender=GrammaticalGender.MASCULINE
)
count_noun_feminine = functools.partial(
    count_noun, grammatical_gender=GrammaticalGender.FEMININE
)
