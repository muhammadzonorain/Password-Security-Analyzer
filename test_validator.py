"""
Unit tests for validator.py
Run with: python -m pytest tests/ -v   (from project root)
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validator import analyze_characters, is_valid_input


def test_detects_all_character_classes():
    report = analyze_characters("Ab1!")
    assert report.has_upper
    assert report.has_lower
    assert report.has_digit
    assert report.has_symbol


def test_length_is_correct():
    report = analyze_characters("password")
    assert report.length == 8


def test_no_uppercase_detected_correctly():
    report = analyze_characters("alllower123")
    assert report.has_upper is False


def test_unique_char_count():
    report = analyze_characters("aabbcc")
    assert report.unique_chars == 3


def test_empty_password_is_invalid():
    valid, msg = is_valid_input("")
    assert valid is False


def test_non_string_is_invalid():
    valid, msg = is_valid_input(12345)
    assert valid is False


def test_normal_password_is_valid():
    valid, msg = is_valid_input("MyP@ssword1")
    assert valid is True


def test_oversized_password_is_invalid():
    valid, msg = is_valid_input("a" * 600)
    assert valid is False
