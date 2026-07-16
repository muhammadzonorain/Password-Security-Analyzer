"""
utils.py
--------
Small, generic helpers that don't belong to a specific analysis module.
"""

import time
from functools import wraps


def timed(func):
    """
    Decorator that measures execution time in milliseconds and passes it
    back via a mutable container, so callers can log/display it without
    changing the wrapped function's return type.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return result, elapsed_ms
    return wrapper
