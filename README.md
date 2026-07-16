# Password Security Analyzer Pro

A command-line password strength checker built for the DecodeLabs
Industrial Training Kit (Project 1 - Defensive Logic track).

The tool goes beyond a simple weak/medium/strong label. It estimates
entropy, flags predictable patterns (sequences, keyboard walks, repeated
characters, known common passwords), gives a 0-100 security score, and
prints an estimated brute-force crack time along with concrete
recommendations.

## Why it exists

The original brief asks for a program that checks length, character
variety, and reports a strength rating. This implementation satisfies
that requirement, then adds the checks a real screening tool would need
so weak-but-varied passwords (like `Qwerty123!`) don't get rated as
"strong" just because every character class is present.

## Features

- Length, uppercase, lowercase, digit, and symbol checks
- Shannon-style entropy estimate (bits) and estimated crack time
- Sequential run detection (`abc`, `123`)
- Repeated character detection (`aaaa`)
- Keyboard-walk detection (`qwerty`, `asdf`)
- Common/breached password lookup against a local wordlist
- Weighted 0-100 score with a visible breakdown
- Plain-language recommendations
- Execution time measurement (confirms the O(n) scan is fast)

## Project structure

```
Password-Security-Analyzer/
├── src/
│   ├── main.py              entry point / CLI loop
│   ├── validator.py         input validation + character checks
│   ├── entropy.py           entropy + crack-time estimation
│   ├── patterns.py          sequence / repeat / keyboard / common-password checks
│   ├── scorer.py            combines everything into a 0-100 score
│   ├── recommendations.py   turns findings into advice
│   ├── report.py            terminal report formatting
│   ├── constants.py         thresholds and weights
│   └── utils.py             timing decorator
├── data/
│   └── common_passwords.txt sample weak/breached password list
├── tests/
│   ├── test_validator.py
│   ├── test_entropy.py
│   └── test_patterns.py
├── docs/
│   └── Project_Report.docx
```

## How it works (pipeline)

```
Input password
      │
      ▼
validator.py    -> is the input usable at all?
      │
      ▼
validator.py    -> which character classes are present? (O(n) scan)
      │
      ▼
entropy.py      -> how many bits of randomness, how long to crack?
      │
      ▼
patterns.py     -> does it match a known weak pattern or breached list?
      │
      ▼
scorer.py       -> combine into a weighted 0-100 score + rating
      │
      ▼
recommendations.py -> translate findings into advice
      │
      ▼
report.py       -> print a formatted result
```

Every stage is a plain function that takes data in and returns data out,
so each one can be unit-tested and reused independently (for example,
`scorer.py` could be swapped out for a different weighting policy
without touching pattern detection).

## Usage

```bash
cd src
python main.py
# then type a password when prompted, or 'exit' to quit

# or, one-shot mode:
python main.py "MyCandidatePassword1!"
```

## Running the tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Scoring model (summary)

| Component        | Max points | Notes                                   |
|-------------------|-----------|------------------------------------------|
| Length            | 25        | 0 below 8 chars, full marks at 16+       |
| Character variety | 25        | lower / upper / digit / symbol, 6.25 each |
| Entropy           | 25        | scaled up to a 60-bit ceiling            |
| Pattern penalty   | up to -25 | sequences, repeats, keyboard walks, common list |

A password that matches the common/breached wordlist is treated as an
automatic critical failure regardless of its other scores, since a
known-leaked password is unsafe no matter how "random" it looks.

## Known limitations

- The entropy model assumes independent, uniformly random characters —
  it will overstate the randomness of predictable-but-varied passwords
  (mitigated, not eliminated, by the pattern penalty).
- The bundled common-password list is a small sample (~50 entries) for
  demonstration. A production system should use a real breach corpus
  such as the "Have I Been Pwned" Pwned Passwords list.
- This tool only *evaluates* password strength; it does not hash, store,
  or transmit passwords, and it should not be treated as a replacement
  for server-side authentication controls.

## Roadmap / stretch goals

- Read the common-password list into a Bloom filter instead of a set,
  so a full breach corpus (millions of entries) fits in memory.
- Add a `--json` output mode for integration into other tools.
- Add a passphrase-aware entropy model (dictionary-word based, not just
  character-based).

## Author

DecodeLabs Industrial Training Kit, Batch 2026 — Project 1.
