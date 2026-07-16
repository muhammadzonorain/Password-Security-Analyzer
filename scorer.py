"""
scorer.py
---------
Combines the outputs of validator.py, entropy.py and patterns.py into a
single 0-100 security score and a Weak / Medium / Strong / Very Strong
classification. This is the "decision" layer described in the project's
IPO (Input -> Process -> Output) model.
"""

from dataclasses import dataclass

from constants import (
    MIN_LENGTH, GOOD_LENGTH, IDEAL_LENGTH,
    WEIGHT_LENGTH, WEIGHT_CHAR_VARIETY, WEIGHT_ENTROPY, WEIGHT_PATTERN_PENALTY_CAP,
    STRENGTH_WEAK, STRENGTH_MEDIUM, STRENGTH_STRONG, STRENGTH_VERY_STRONG,
)
from validator import CharacterReport
from patterns import PatternReport


@dataclass
class ScoreResult:
    score: int
    strength: str
    breakdown: dict


def _score_length(length: int) -> float:
    """Linear ramp: 0 points below MIN_LENGTH, full points at IDEAL_LENGTH+."""
    if length < MIN_LENGTH:
        return 0.0
    if length >= IDEAL_LENGTH:
        return WEIGHT_LENGTH
    if length >= GOOD_LENGTH:
        # scale between GOOD_LENGTH and IDEAL_LENGTH
        fraction = (length - GOOD_LENGTH) / (IDEAL_LENGTH - GOOD_LENGTH)
        return WEIGHT_LENGTH * (0.7 + 0.3 * fraction)
    # scale between MIN_LENGTH and GOOD_LENGTH
    fraction = (length - MIN_LENGTH) / (GOOD_LENGTH - MIN_LENGTH)
    return WEIGHT_LENGTH * (0.4 * fraction)


def _score_char_variety(report: CharacterReport) -> float:
    """One quarter of the variety weight per character class present."""
    classes_present = sum([report.has_lower, report.has_upper, report.has_digit, report.has_symbol])
    return WEIGHT_CHAR_VARIETY * (classes_present / 4)


def _score_entropy(entropy_bits: float) -> float:
    """
    Full entropy points at 60+ bits (roughly equivalent to a 12-character
    password drawn from a 60+ symbol pool), scaled linearly below that.
    """
    ENTROPY_CEILING = 60.0
    fraction = min(entropy_bits / ENTROPY_CEILING, 1.0)
    return WEIGHT_ENTROPY * fraction


def _pattern_penalty(pattern_report: PatternReport) -> float:
    """
    Each detected weakness removes points, capped so a single flaw can't
    push the score below zero on its own.
    """
    penalty_per_hit = WEIGHT_PATTERN_PENALTY_CAP / 4  # 4 possible pattern flags
    hits = sum([
        pattern_report.is_common_password,
        pattern_report.has_sequential_run,
        pattern_report.has_repeated_run,
        pattern_report.has_keyboard_walk,
    ])
    # A known common/breached password is treated as an automatic critical failure.
    if pattern_report.is_common_password:
        return WEIGHT_PATTERN_PENALTY_CAP
    return min(hits * penalty_per_hit, WEIGHT_PATTERN_PENALTY_CAP)


def classify(score: int, length: int) -> str:
    """Map the numeric score onto a strength label, with length as a hard gate."""
    if length < MIN_LENGTH:
        return STRENGTH_WEAK
    if score < 40:
        return STRENGTH_WEAK
    if score < 65:
        return STRENGTH_MEDIUM
    if score < 85:
        return STRENGTH_STRONG
    return STRENGTH_VERY_STRONG


def calculate_score(
    char_report: CharacterReport,
    entropy_bits: float,
    pattern_report: PatternReport,
) -> ScoreResult:
    length_pts = _score_length(char_report.length)
    variety_pts = _score_char_variety(char_report)
    entropy_pts = _score_entropy(entropy_bits)
    penalty = _pattern_penalty(pattern_report)

    raw_score = length_pts + variety_pts + entropy_pts - penalty
    final_score = max(0, min(100, round(raw_score)))

    strength = classify(final_score, char_report.length)

    breakdown = {
        "length_points": round(length_pts, 1),
        "variety_points": round(variety_pts, 1),
        "entropy_points": round(entropy_pts, 1),
        "pattern_penalty": round(penalty, 1),
    }

    return ScoreResult(score=final_score, strength=strength, breakdown=breakdown)
