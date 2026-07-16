"""
main.py
-------
Password Security Analyzer Pro
DecodeLabs Industrial Training Kit - Project 1

Entry point. Wires together validator -> entropy -> patterns -> scorer
-> recommendations -> report, following the Input -> Process -> Output
model described in the project brief. Run directly:

    python src/main.py
"""

import sys

from validator import is_valid_input, analyze_characters
from entropy import calculate_entropy_bits, estimate_crack_time_seconds
from patterns import analyze_patterns
from scorer import calculate_score
from recommendations import build_recommendations
from report import render_report, mask_password
from utils import timed


@timed
def run_analysis(password: str):
    """
    Runs the full pipeline once and returns everything a caller needs to
    render a report. Wrapped in @timed so main() can report performance
    without cluttering this function with stopwatch code.
    """
    char_report = analyze_characters(password)
    entropy_bits = calculate_entropy_bits(password, char_report)
    crack_seconds = estimate_crack_time_seconds(entropy_bits)
    pattern_report = analyze_patterns(password)
    score_result = calculate_score(char_report, entropy_bits, pattern_report)
    recommendations = build_recommendations(char_report, pattern_report)

    return {
        "char_report": char_report,
        "entropy_bits": entropy_bits,
        "crack_seconds": crack_seconds,
        "pattern_report": pattern_report,
        "score_result": score_result,
        "recommendations": recommendations,
    }


def analyze_and_print(password: str) -> None:
    valid, error_message = is_valid_input(password)
    if not valid:
        print(f"[!] Invalid input: {error_message}")
        return

    result, elapsed_ms = run_analysis(password)

    output = render_report(
        password_masked=mask_password(password),
        char_report=result["char_report"],
        entropy_bits=result["entropy_bits"],
        crack_seconds=result["crack_seconds"],
        pattern_report=result["pattern_report"],
        score_result=result["score_result"],
        recommendations=result["recommendations"],
        elapsed_ms=elapsed_ms,
    )
    print(output)


def print_banner() -> None:
    print("=" * 56)
    print(" PASSWORD SECURITY ANALYZER PRO v1.0")
    print(" DecodeLabs Industrial Training Kit - Project 1")
    print("=" * 56)
    print(" Type a password to analyze it, or 'exit' to quit.")
    print("=" * 56)


def main() -> None:
    # Support: python main.py "SomePassword123!" for one-shot / scripted use.
    if len(sys.argv) > 1:
        analyze_and_print(sys.argv[1])
        return

    print_banner()
    while True:
        try:
            password = input("\nEnter password to analyze: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting. Stay secure.")
            break

        if password.strip().lower() == "exit":
            print("Exiting. Stay secure.")
            break

        analyze_and_print(password)


if __name__ == "__main__":
    main()
