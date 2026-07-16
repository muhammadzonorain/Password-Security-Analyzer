"""
validator.py
------------
Lowest layer of the analyzer. Pure string-handling and conditional
checks — no scoring, no entropy math. This is deliberately kept simple
so it maps directly onto the "Key Requirements" from the project brief:

    * Check password length
    * Check use of numbers, symbols, and uppercase letters
"""

import string
from dataclasses import dataclass


@dataclass
class CharacterReport:
    """Holds the outcome of every basic character-class check."""
    length: int
    has_lower: bool
    has_upper: bool
    has_digit: bool
    has_symbol: bool
    has_space: bool
    unique_chars: int


def analyze_characters(password: str) -> CharacterReport:
    """
    Walk the password once (O(n)) and classify every character.

    Using generator expressions with any() lets Python's C implementation
    do the looping and short-circuit as soon as a match is found, which is
    faster and more readable than a manual for-loop with a flag variable.
    """
    return CharacterReport(
        length=len(password),
        has_lower=any(c.islower() for c in password),
        has_upper=any(c.isupper() for c in password),
        has_digit=any(c.isdigit() for c in password),
        has_symbol=any(c in string.punctuation for c in password),
        has_space=any(c.isspace() for c in password),
        unique_chars=len(set(password)),
    )


def is_valid_input(password: str) -> tuple[bool, str]:
    """
    Guard against inputs that would break downstream logic:
    empty strings, non-string types, or absurdly long input used as a
    denial-of-service vector against the analyzer itself.
    """
    if not isinstance(password, str):
        return False, "Password must be a text string."
    if len(password) == 0:
        return False, "Password cannot be empty."
    if len(password) > 512:
        return False, "Password exceeds the maximum supported length (512 characters)."
    return True, ""
