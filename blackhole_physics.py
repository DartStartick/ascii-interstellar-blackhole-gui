"""Physics simulation for the ASCII black hole.

This module contains placeholder classes and functions to compute
how light bends around a black hole and how the accretion disk
should appear. For now the calculations are stubbed out.
"""

from typing import List

import math

from utils import clamp

class BlackHoleSimulator:
    """Compute frames representing the black hole's appearance."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Placeholder parameters controlling the accretion disk and rotation.
        self.disk_radius = 0.4  # Relative to half the smallest dimension
        self.disk_width = 0.1
        self.angular_velocity = 0.05  # Radians per frame
        self.phase = 0.0

    def compute_frame(self) -> List[List[float]]:
        """Return a brightness matrix for the current frame."""

        # Normalise coordinates so that the shorter side spans -1..1.
        scale = 2.0 / min(self.width, self.height)
        cx = self.width / 2.0
        cy = self.height / 2.0

        frame: List[List[float]] = []
        for y in range(self.height):
            row: List[float] = []
            dy = (y - cy) * scale
            for x in range(self.width):
                dx = (x - cx) * scale
                r = math.hypot(dx, dy)
                phi = math.atan2(dy, dx) + self.phase

                # Simple accretion disk brightness profile.
                disk = math.exp(-((r - self.disk_radius) ** 2) / (2 * self.disk_width ** 2))

                # Add a swirl pattern to mimic rotation of matter.
                swirl = 0.5 + 0.5 * math.sin(8 * phi - r * 10)

                brightness = clamp(disk * swirl, 0.0, 1.0)
                row.append(brightness)
            frame.append(row)

        # Advance phase for animation.
        self.phase += self.angular_velocity

        return frame
