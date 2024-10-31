import enum
import functools


class InvalidNumberError(Exception):
    """Exception raised when a number cannot be represented."""


class GrammaticalGender(enum.StrEnum):
    """
    Represents grammatical gender (מין דקדוקי).

    Attributes:
        FEMININE: Feminine form (צורת הנקבה), e.g., "שלוש ילדות".
        MASCULINE: Masculine form (צורת הזכר), e.g., "שלושה ילדים".

    """

    FEMININE = "f"
    MASCULINE = "m"


class ConstructState(enum.Enum):
    """
    Represents the construct state (צורת נסמך) in grammar.

    Attributes:
        ABSOLUTE: Absolute form (צורת הנפרד), e.g., "שלושה ילדים".
        CONSTRUCT: Construct form (צורת הנסמך), e.g., "שלושת הילדים".

    """

    ABSOLUTE = False
    CONSTRUCT = True


def _join_words(
    words: list[str], sep: str = " ", last_sep: str = " ו"  # noqa: RUF001
) -> str:
    """
    Combine all words in the list into a single string.

    Words are separated by `sep`, with the final pair separated by `last_sep`.
    """
    words = [w for w in words if w]
    if not words:
        raise ValueError("The 'words' list must contain at least one non-empty string")
    if len(words) == 1:
        return words[0]
    return f"{sep.join(words[:-1])}{last_sep}{words[-1]}"


def _translate_one_digit(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> str:
    """Translate a single digit (1-9) into the corresponding Hebrew word."""
    if not 1 <= n <= 9:  # noqa: PLR2004
        raise ValueError("The number must be an integer between 1 and 9")
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
    raise ValueError("Invalid grammatical_gender or construct_state provided")


def _translate_to_20(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> str:
    """Translate a number from 1 to 19 into the corresponding Hebrew word."""
    if not 1 <= n <= 19:  # noqa: PLR2004
        raise ValueError("The number must be between 1 and 19")
    if n < 10:  # noqa: PLR2004
        return _translate_one_digit(n, grammatical_gender, construct_state)
    if n == 10:  # noqa: PLR2004
        return {
            (GrammaticalGender.FEMININE, ConstructState.ABSOLUTE): "עשר",
            (GrammaticalGender.FEMININE, ConstructState.CONSTRUCT): "עשר",
            (GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE): "עשרה",
            (GrammaticalGender.MASCULINE, ConstructState.CONSTRUCT): "עשרת",
        }[grammatical_gender, construct_state]
    # GRAMMAR RULE: weird exceptions for 11 and 12
    if n == 11:  # noqa: PLR2004
        n_str = _translate_one_digit(
            n % 10, grammatical_gender, ConstructState.CONSTRUCT
        )
    elif n == 12:  # noqa: PLR2004
        n_str = {
            GrammaticalGender.FEMININE: "שתים",
            GrammaticalGender.MASCULINE: "שנים",
        }[grammatical_gender]
    else:
        n_str = _translate_one_digit(
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


def _decompose_hundreds(
    n: int, grammatical_gender: GrammaticalGender, construct_state: ConstructState
) -> list[str]:
    """
    Translate a number from 1 to 999 into a list of Hebrew words.

    Words represent the hundreds, tens, and units.
    """
    if not 1 <= n <= 999:  # noqa: PLR2004
        raise ValueError("The number must be between 1 and 999")
    hundreds_digit = n // 100
    if hundreds_digit == 0:
        hundreds_word = ""
    elif hundreds_digit == 1:
        hundreds_word = "מאה"
    elif hundreds_digit == 2:  # noqa: PLR2004
        hundreds_word = "מאתיים"
    else:
        # GRAMMAR RULE: construct_state is always used for hundreds
        hundreds_word = (
            _translate_one_digit(
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
        # GRAMMAR RULE: construct_state is applied only up to 20
        last_digits_word = _translate_to_20(
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
    """
    Translate a positive integer into Hebrew words as a cardinal number (מספר מונה).

    This function respects grammatical gender (masculine, feminine) and construct state
    (absolute, construct).

    Supports non-negative integers up to 10^21.
    """
    if n >= 1_000_000_000_000_000_000 * 1000:
        raise InvalidNumberError("Numbers must be below 10^21")
    if n < 0:
        raise InvalidNumberError("Negative numbers do not have a valid representation")
    if n == 0:
        if construct_state == ConstructState.CONSTRUCT:
            raise InvalidNumberError("Zero does not have a construct form")
        return "אפס"

    def add_suffix(n: int, suffix: str, grammatical_gender: GrammaticalGender) -> str:
        if n == 0:
            return ""
        if n == 1:
            return suffix
        # GRAMMAR RULE: construct_state is not used for 10^6 and above
        n_str = _join_words(
            _decompose_hundreds(n, grammatical_gender, ConstructState.ABSOLUTE)
        )
        return f"{n_str} {suffix}"

    quintillions = n // 1_000_000_000_000_000_000 % 1000
    quintillions_word = add_suffix(
        quintillions, "קווינטיליון", GrammaticalGender.MASCULINE
    )

    quadrillions = n // 1_000_000_000_000_000 % 1000
    quadrillions_word = add_suffix(
        quadrillions, "קוודריליון", GrammaticalGender.MASCULINE
    )

    trillions = n // 1_000_000_000_000 % 1000
    trillions_word = add_suffix(trillions, "טריליון", GrammaticalGender.MASCULINE)

    billions = n // 1_000_000_000 % 1000
    billions_word = add_suffix(billions, "מיליארד", GrammaticalGender.MASCULINE)

    millions = n // 1_000_000 % 1000
    millions_word = add_suffix(millions, "מיליון", GrammaticalGender.MASCULINE)

    thousands = n // 1_000 % 1000
    if thousands == 0:
        thousands_word = ""
    elif thousands == 1:
        thousands_word = "אלף"
    elif thousands == 2:  # noqa: PLR2004
        thousands_word = "אלפיים"
    # GRAMMAR RULE: construct_state is used for 1000 only up to 10
    elif thousands <= 10:  # noqa: PLR2004
        thousands_word = (
            _join_words(
                _decompose_hundreds(
                    thousands, GrammaticalGender.MASCULINE, ConstructState.CONSTRUCT
                )
            )
            + " אלפים"
        )
    else:
        thousands_word = (
            _join_words(
                _decompose_hundreds(
                    thousands, GrammaticalGender.MASCULINE, ConstructState.ABSOLUTE
                )
            )
            + " אלף"
        )

    last_digits = n % 1_000
    if last_digits == 0:
        last_digits_words = []
    else:
        # GRAMMAR RULE: construct_state is applied only up to 20
        last_digits_words = _decompose_hundreds(
            last_digits,
            grammatical_gender,
            construct_state if n < 1000 else ConstructState.ABSOLUTE,  # noqa: PLR2004
        )

    words = [
        quintillions_word,
        quadrillions_word,
        trillions_word,
        billions_word,
        millions_word,
        thousands_word,
        *last_digits_words,
    ]
    return _join_words(words)


# מספר מונה
def cardinal_number(
    n: int, grammatical_gender: GrammaticalGender, *, is_definite_noun: bool = False
) -> str:
    """
    Generate a Hebrew cardinal number (מספר מונה) suitable as a prefix before a noun.

    Chooses the correct construct state based on whether the noun is definite or
    indefinite (שם עצם מיודע/לא מיודע).
    Supports non-negative integers up to 10^21.
    Does not support `n = 1`, as a singular item is not using a prefix.
    """
    if n < 0:
        raise InvalidNumberError("The number must be non-negative")
    if n == 1:
        raise InvalidNumberError("The value '1' cannot be used as a prefix for a noun")
    # GRAMMAR RULE: always using construct form for 2
    if n == 2:  # noqa: PLR2004
        construct_state = ConstructState.CONSTRUCT
    # GRAMMAR RULE: never using construct form for numbers above 10
    elif n > 10:  # noqa: PLR2004
        construct_state = ConstructState.ABSOLUTE
    else:
        construct_state = (
            ConstructState.CONSTRUCT if is_definite_noun else ConstructState.ABSOLUTE
        )
    return number(n, grammatical_gender, construct_state)


def count_noun(
    n: int,
    singular_form: str,
    plural_form: str,
    grammatical_gender: GrammaticalGender,
    *,
    is_definite_noun: bool = False,
) -> str:
    """
    Generate a Hebrew phrase for counting a noun, handling singular and plural forms.

    Chooses the appropriate form based on `n` and adjusts for grammatical gender
    and definiteness.
    Supports non-negative integers up to 10^21.
    """
    if n == 1:
        n_str = ("ה" if is_definite_noun else "") + number(
            n,
            grammatical_gender,
            ConstructState.ABSOLUTE,
        )
        return f"{singular_form} {n_str}"
    n_str = cardinal_number(n, grammatical_gender, is_definite_noun=is_definite_noun)
    return f"{n_str} {plural_form}"


def indefinite_number(n: int) -> str:
    """
    Create a string representing an indefinite number (מספר סתמי).

    For negative numbers, the string will include a "minus" prefix (מינוס).
    Supports integers up to 10^21.
    """
    if n < 0:
        n_str = number(-n, GrammaticalGender.FEMININE, ConstructState.ABSOLUTE)
        return f"מינוס {n_str}"
    return number(n, GrammaticalGender.FEMININE, ConstructState.ABSOLUTE)


def ordinal_number(n: int, grammatical_gender: GrammaticalGender) -> str:
    """
    Create a string representing an ordinal number (מספר סודר).

    Supports positive integers up to 10^21.
    """
    if n <= 0:
        raise InvalidNumberError("Ordinal numbers must be positive integers")
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
    raise ValueError("Invalid grammatical_gender provided")


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
