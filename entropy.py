"""
entropy.py
----------
Estimates password entropy (bits of randomness) and converts that into
a rough "time to crack" figure. This is a simplified model — real-world
entropy also depends on dictionary/pattern predictability, which is
handled separately in patterns.py and folded into the final score.
"""

import math

from constants import (
    POOL_LOWER, POOL_UPPER, POOL_DIGIT, POOL_SYMBOL,
    ATTACKER_GUESSES_PER_SECOND,
)
from validator import CharacterReport


def estimate_pool_size(report: CharacterReport) -> int:
    """
    Work out how large the character set 'space' is, based on which
    classes of character are actually present. A password only made of
    lowercase letters has a pool of 26; add digits and it becomes 36, etc.
    """
    pool = 0
    if report.has_lower:
        pool += POOL_LOWER
    if report.has_upper:
        pool += POOL_UPPER
    if report.has_digit:
        pool += POOL_DIGIT
    if report.has_symbol:
        pool += POOL_SYMBOL
    return max(pool, 1)  # avoid log(0) if somehow nothing matched


def calculate_entropy_bits(password: str, report: CharacterReport) -> float:
    """
    Shannon-style entropy approximation: bits = length * log2(pool_size).

    This assumes each character was chosen independently and uniformly at
    random from the pool, which overstates entropy for human-chosen
    passwords (hence why pattern detection is applied separately).
    """
    pool_size = estimate_pool_size(report)
    return round(report.length * math.log2(pool_size), 2)


def estimate_crack_time_seconds(entropy_bits: float) -> float:
    """
    Convert entropy into an estimated offline brute-force time, assuming
    an attacker needs to search half the key space on average.
    """
    total_combinations = 2 ** entropy_bits
    return total_combinations / (2 * ATTACKER_GUESSES_PER_SECOND)


def humanize_seconds(seconds: float) -> str:
    """Turn a raw seconds figure into a readable duration string."""
    if seconds < 1:
        return "instantly"

    units = [
        ("centuries", 60 * 60 * 24 * 365 * 100),
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
        ("seconds", 1),
    ]
    for name, unit_seconds in units:
        value = seconds / unit_seconds
        if value >= 1:
            if name == "centuries" and value > 1_000_000:
                return "longer than the age of the universe"
            return f"~{value:,.1f} {name}"
    return "instantly"
