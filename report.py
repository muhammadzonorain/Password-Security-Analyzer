"""
report.py
---------
Formats the full analysis result as readable terminal output. Kept
separate from main.py so the same underlying data could later be
rendered as JSON, HTML, or a GUI without touching the analysis logic.
"""

from entropy import humanize_seconds


def render_report(
    password_masked: str,
    char_report,
    entropy_bits: float,
    crack_seconds: float,
    pattern_report,
    score_result,
    recommendations,
    elapsed_ms: float,
) -> str:
    lines = []
    line = "-" * 56

    lines.append(line)
    lines.append("PASSWORD SECURITY ANALYZER - RESULT")
    lines.append(line)
    lines.append(f"Password (masked):   {password_masked}")
    lines.append(f"Length:              {char_report.length}")
    lines.append(f"Uppercase present:   {'Yes' if char_report.has_upper else 'No'}")
    lines.append(f"Lowercase present:   {'Yes' if char_report.has_lower else 'No'}")
    lines.append(f"Digit present:       {'Yes' if char_report.has_digit else 'No'}")
    lines.append(f"Symbol present:      {'Yes' if char_report.has_symbol else 'No'}")
    lines.append(f"Unique characters:   {char_report.unique_chars}")
    lines.append(line)
    lines.append(f"Estimated entropy:   {entropy_bits} bits")
    lines.append(f"Est. crack time:     {humanize_seconds(crack_seconds)}")
    lines.append(line)

    if pattern_report.reasons:
        lines.append("Pattern warnings:")
        for reason in pattern_report.reasons:
            lines.append(f"  - {reason}")
    else:
        lines.append("Pattern warnings:    None detected")
    lines.append(line)

    lines.append(f"Score breakdown:")
    for key, value in score_result.breakdown.items():
        lines.append(f"  {key.replace('_', ' ').title():<20}: {value}")
    lines.append(line)
    lines.append(f"FINAL SCORE:         {score_result.score} / 100")
    lines.append(f"STRENGTH RATING:     {score_result.strength.upper()}")
    lines.append(line)

    lines.append("Recommendations:")
    for tip in recommendations:
        lines.append(f"  * {tip}")
    lines.append(line)

    lines.append(f"Analysis completed in {elapsed_ms:.3f} ms")
    lines.append(line)

    return "\n".join(lines)


def mask_password(password: str) -> str:
    """Show only the first and last character, mask the rest, for safe display."""
    if len(password) <= 2:
        return "*" * len(password)
    return password[0] + "*" * (len(password) - 2) + password[-1]
