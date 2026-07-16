"""
patterns.py
-----------
Detects predictable structures that make a password weaker than its raw
entropy suggests: sequential runs (abc, 123), repeated characters
(aaaa), keyboard walks (qwerty, asdfgh), and membership in a list of
known breached/common passwords.
"""

import os
from dataclasses import dataclass, field

from constants import KEYBOARD_ROWS, COMMON_PASSWORDS_FILE


@dataclass
class PatternReport:
    is_common_password: bool = False
    has_sequential_run: bool = False
    has_repeated_run: bool = False
    has_keyboard_walk: bool = False
    reasons: list = field(default_factory=list)


def _load_common_passwords() -> set:
    """
    Load the local common-password wordlist into a set for O(1) lookups.
    Falls back to an empty set if the data file is missing, so the rest
    of the analyzer keeps working even without the wordlist installed.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, COMMON_PASSWORDS_FILE)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


_COMMON_PASSWORDS = _load_common_passwords()


def has_sequential_run(password: str, run_length: int = 3) -> bool:
    """
    Detect ascending or descending runs of consecutive characters,
    e.g. 'abc', 'cba', '123', '321'. Works on character code points so
    it catches letters and digits with the same logic.
    """
    lowered = password.lower()
    for i in range(len(lowered) - run_length + 1):
        window = lowered[i:i + run_length]
        codes = [ord(c) for c in window]
        ascending = all(codes[j] + 1 == codes[j + 1] for j in range(len(codes) - 1))
        descending = all(codes[j] - 1 == codes[j + 1] for j in range(len(codes) - 1))
        if ascending or descending:
            return True
    return False


def has_repeated_run(password: str, run_length: int = 3) -> bool:
    """Detect the same character repeated run_length+ times in a row, e.g. 'aaa'."""
    for i in range(len(password) - run_length + 1):
        window = password[i:i + run_length]
        if len(set(window.lower())) == 1:
            return True
    return False


def has_keyboard_walk(password: str, run_length: int = 4) -> bool:
    """Detect substrings that follow a straight line on a QWERTY keyboard."""
    lowered = password.lower()
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - run_length + 1):
            fragment = row[i:i + run_length]
            if fragment in lowered or fragment[::-1] in lowered:
                return True
    return False


def is_common_password(password: str) -> bool:
    """Check membership against the loaded common/breached password set."""
    return password.lower() in _COMMON_PASSWORDS


def analyze_patterns(password: str) -> PatternReport:
    """Run every pattern check and collect a human-readable reason for each hit."""
    report = PatternReport()

    if is_common_password(password):
        report.is_common_password = True
        report.reasons.append("Matches a known common/breached password.")

    if has_sequential_run(password):
        report.has_sequential_run = True
        report.reasons.append("Contains a sequential character run (e.g. 'abc', '123').")

    if has_repeated_run(password):
        report.has_repeated_run = True
        report.reasons.append("Contains a repeated character run (e.g. 'aaa').")

    if has_keyboard_walk(password):
        report.has_keyboard_walk = True
        report.reasons.append("Contains a keyboard-adjacent pattern (e.g. 'qwerty', 'asdf').")

    return report
