"""Utility helpers for the project."""

from typing import Iterable, List, Sequence

import math


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


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between ``a`` and ``b``."""
    return a + (b - a) * t


def map_range(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float = 0.0,
    out_max: float = 1.0,
) -> float:
    """Map ``value`` from one range to another."""
    if in_max - in_min == 0:
        return out_min
    ratio = (value - in_min) / (in_max - in_min)
    return lerp(out_min, out_max, clamp(ratio, 0.0, 1.0))


def length(v: Sequence[float]) -> float:
    """Return the Euclidean length of a vector."""
    return math.sqrt(sum(c * c for c in v))


def normalize_vector(v: Sequence[float]) -> List[float]:
    """Return a unit vector in the direction of ``v``."""
    l = length(v)
    if l == 0:
        return [0.0 for _ in v]
    return [c / l for c in v]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """Dot product of two 3D vectors."""
    return sum(x * y for x, y in zip(a, b))


def cross(a: Sequence[float], b: Sequence[float]) -> List[float]:
    """Cross product of two 3D vectors."""
    ax, ay, az = a
    bx, by, bz = b
    return [ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx]


def rotate_x(v: Sequence[float], angle: float) -> List[float]:
    """Rotate ``v`` around the X axis by ``angle`` radians."""
    x, y, z = v
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]


def rotate_y(v: Sequence[float], angle: float) -> List[float]:
    """Rotate ``v`` around the Y axis by ``angle`` radians."""
    x, y, z = v
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a]


def rotate_z(v: Sequence[float], angle: float) -> List[float]:
    """Rotate ``v`` around the Z axis by ``angle`` radians."""
    x, y, z = v
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x * cos_a - y * sin_a, x * sin_a + y * cos_a, z]
