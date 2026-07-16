"""
recommendations.py
-------------------
Turns the raw analysis results into plain-language advice for the user.
Kept separate from scoring so the "what to say" logic can change without
touching the "how to score" logic.
"""

from constants import MIN_LENGTH, GOOD_LENGTH
from validator import CharacterReport
from patterns import PatternReport


def build_recommendations(char_report: CharacterReport, pattern_report: PatternReport) -> list:
    tips = []

    if char_report.length < MIN_LENGTH:
        tips.append(f"Increase length to at least {MIN_LENGTH} characters.")
    elif char_report.length < GOOD_LENGTH:
        tips.append(f"Consider extending to {GOOD_LENGTH}+ characters for stronger protection.")

    if not char_report.has_upper:
        tips.append("Add at least one uppercase letter (A-Z).")
    if not char_report.has_lower:
        tips.append("Add at least one lowercase letter (a-z).")
    if not char_report.has_digit:
        tips.append("Add at least one digit (0-9).")
    if not char_report.has_symbol:
        tips.append("Add at least one special character (e.g. ! @ # $ %).")

    if pattern_report.is_common_password:
        tips.append("This password appears in known breach/common-password lists — replace it entirely.")
    if pattern_report.has_sequential_run:
        tips.append("Avoid sequential runs like 'abc' or '123'.")
    if pattern_report.has_repeated_run:
        tips.append("Avoid repeating the same character multiple times in a row.")
    if pattern_report.has_keyboard_walk:
        tips.append("Avoid keyboard patterns like 'qwerty' or 'asdf'.")

    if not tips:
        tips.append("No major weaknesses detected. Consider using a passphrase or password manager for even stronger, unique credentials.")

    return tips
