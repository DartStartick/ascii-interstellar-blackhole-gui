"""Physics simulation for the ASCII black hole.

This module contains placeholder classes and functions to compute
how light bends around a black hole and how the accretion disk
should appear. For now the calculations are stubbed out.
"""

from typing import List

class BlackHoleSimulator:
    """Compute frames representing the black hole's appearance."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Future parameters like mass, spin, etc. will go here

    def compute_frame(self) -> List[List[float]]:
        """Return a dummy brightness matrix for the current frame."""
        return [[0.0 for _ in range(self.width)] for _ in range(self.height)]
