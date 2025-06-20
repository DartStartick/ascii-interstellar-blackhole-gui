"""Utility helpers for the project."""

from typing import Iterable


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value to the given range."""
    return max(min_value, min(value, max_value))


def normalize(values: Iterable[float]) -> Iterable[float]:
    """Normalize an iterable of values to the 0..1 range."""
    lst = list(values)
    if not lst:
        return lst
    min_v, max_v = min(lst), max(lst)
    span = max_v - min_v or 1
    return [(v - min_v) / span for v in lst]
