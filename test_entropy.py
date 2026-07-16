import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validator import analyze_characters
from entropy import calculate_entropy_bits, estimate_pool_size, humanize_seconds


def test_pool_size_grows_with_variety():
    lower_only = analyze_characters("abcdef")
    mixed = analyze_characters("aB3!ef")
    assert estimate_pool_size(mixed) > estimate_pool_size(lower_only)


def test_longer_password_has_more_entropy():
    short = analyze_characters("Abcdef1!")
    long = analyze_characters("Abcdef1!Abcdef1!")
    e_short = calculate_entropy_bits("Abcdef1!", short)
    e_long = calculate_entropy_bits("Abcdef1!Abcdef1!", long)
    assert e_long > e_short


def test_humanize_seconds_instant():
    assert humanize_seconds(0.001) == "instantly"


def test_humanize_seconds_years():
    result = humanize_seconds(60 * 60 * 24 * 365 * 5)
    assert "years" in result
