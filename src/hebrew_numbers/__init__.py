"""hebrew-numbers: Convert numbers to Hebrew.

Copyright (c) 2025 Tsvika Shapira. All rights reserved.
"""

from ._version import version as _version
from .hebrew_numbers import (
    ConstructState,
    GrammaticalGender,
    InvalidNumberError,
    cardinal_number,
    count_noun,
    count_prefix,
    indefinite_number,
    ordinal_number,
)

__version__ = _version
__all__ = [
    "ConstructState",
    "GrammaticalGender",
    "InvalidNumberError",
    "cardinal_number",
    "count_noun",
    "count_prefix",
    "indefinite_number",
    "ordinal_number",
]
