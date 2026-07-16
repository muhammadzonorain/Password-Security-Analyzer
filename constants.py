"""
constants.py
------------
Central place for every tunable value used across the analyzer.
Keeping these in one module means the scoring policy can be adjusted
without touching the logic that consumes it.
"""

# --- Length policy -----------------------------------------------------
MIN_LENGTH = 8          # anything shorter is an automatic fail (NIST-ish baseline)
GOOD_LENGTH = 12         # length that starts earning bonus points
IDEAL_LENGTH = 16        # length that earns full length points

# --- Scoring weights (must add up to 100) -------------------------------
WEIGHT_LENGTH = 25
WEIGHT_CHAR_VARIETY = 25
WEIGHT_ENTROPY = 25
WEIGHT_PATTERN_PENALTY_CAP = 25   # patterns/breaches can remove up to this many points

# --- Strength labels -----------------------------------------------------
STRENGTH_WEAK = "Weak"
STRENGTH_MEDIUM = "Medium"
STRENGTH_STRONG = "Strong"
STRENGTH_VERY_STRONG = "Very Strong"

# --- Character pools (used for entropy calculation) ----------------------
POOL_LOWER = 26
POOL_UPPER = 26
POOL_DIGIT = 10
POOL_SYMBOL = 33   # printable ASCII punctuation

# --- Keyboard walk patterns to detect (QWERTY rows) -----------------------
KEYBOARD_ROWS = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "1234567890",
]

# --- Common weak passwords (small local sample; production systems should
#     use the full "Have I Been Pwned" list, ~10 million+ entries) ---------
COMMON_PASSWORDS_FILE = "data/common_passwords.txt"

# --- Brute-force assumptions ----------------------------------------------
# Guesses per second an offline attacker with a modern GPU rig is assumed
# to achieve against a slow, salted hash (order-of-magnitude estimate only).
ATTACKER_GUESSES_PER_SECOND = 10_000_000_000  # 10 billion/s
