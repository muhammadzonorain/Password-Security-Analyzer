import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from patterns import (
    has_sequential_run, has_repeated_run, has_keyboard_walk,
    is_common_password, analyze_patterns,
)


def test_sequential_run_ascending():
    assert has_sequential_run("xy9abc12") is True


def test_sequential_run_descending():
    assert has_sequential_run("cbaXYZ") is True


def test_no_sequential_run():
    assert has_sequential_run("xk4mQz9p") is False


def test_repeated_run_detected():
    assert has_repeated_run("Heyyyy123") is True


def test_repeated_run_not_falsely_detected():
    assert has_repeated_run("Kj3nP9qL") is False


def test_keyboard_walk_detected():
    assert has_keyboard_walk("myqwertypass") is True


def test_common_password_detected():
    assert is_common_password("123456") is True


def test_uncommon_password_not_flagged():
    assert is_common_password("Xk9#mQ2vLp") is False


def test_analyze_patterns_collects_reasons():
    report = analyze_patterns("qwerty123")
    assert report.has_keyboard_walk is True
    assert report.has_sequential_run is True
    assert len(report.reasons) >= 2
