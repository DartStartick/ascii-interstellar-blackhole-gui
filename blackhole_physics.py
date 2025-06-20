"""Physics simulation for the ASCII black hole.

This module implements a very small ray tracer that mimics
gravitational lensing around a Schwarzschild black hole.
The goal is not absolute physical accuracy, but rather to
produce the characteristic "Interstellar" look where light
from the accretion disk is bent over and under the event
horizon.
"""

from typing import List

import math

from utils import clamp
import config


def _normalize(v: List[float]) -> List[float]:
    """Return a unit vector in the direction of ``v``."""
    length = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / length for c in v]


def _rotate_x(v: List[float], angle: float) -> List[float]:
    """Rotate ``v`` around the X axis by ``angle`` radians."""
    x, y, z = v
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

class BlackHoleSimulator:
    """Generate brightness frames using a simple ray-marching approach."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        # Camera and black hole parameters.  All units are arbitrary but
        # consistent so the simulation looks plausible.
        self.camera_distance = 8.0
        self.camera_pitch = config.CAMERA_PITCH
        self.bh_radius = 1.0
        self.mass = 1.0  # Controls lensing strength

        # Accretion disk characteristics
        self.disk_inner = 3.0
        self.disk_outer = 5.0
        self.disk_thickness = 0.05

        # Visual tweaks
        self.angular_velocity = 0.03  # Disk rotation speed (radians per frame)
        self.phase = 0.0
        self.step_size = 0.02
        self.max_steps = 500

    def compute_frame(self) -> List[List[float]]:
        """Return a brightness matrix for the current frame."""

        # Normalise coordinates so the shorter side spans roughly [-1, 1].
        scale = 2.0 / min(self.width, self.height)
        cx = self.width / 2.0
        cy = self.height / 2.0

        frame: List[List[float]] = []
        for iy in range(self.height):
            row: List[float] = []
            dy = (iy - cy) * scale
            for ix in range(self.width):
                dx = (ix - cx) * scale
                b = self._trace_pixel(dx, dy)
                row.append(b)
            frame.append(row)

        self.phase += self.angular_velocity
        return frame

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _trace_pixel(self, x: float, y: float) -> float:
        """Trace a single pixel and return its brightness."""
        # Ray origin and direction in camera space
        origin = _rotate_x([0.0, 0.0, self.camera_distance], self.camera_pitch)
        direction = _normalize([x, y, -self.camera_distance])
        direction = _rotate_x(direction, self.camera_pitch)

        pos = origin[:]
        dir_vec = direction[:]

        for _ in range(self.max_steps):
            # Distance from black hole centre
            r = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
            if r < self.bh_radius:
                return 0.0

            # Check intersection with the disk plane (y ~= 0)
            if abs(pos[1]) < self.disk_thickness:
                radial = math.hypot(pos[0], pos[2])
                if self.disk_inner <= radial <= self.disk_outer:
                    phi = math.atan2(pos[2], pos[0]) + self.phase
                    base = math.exp(-((radial - self.disk_inner) / (self.disk_outer - self.disk_inner)) ** 2)
                    swirl = 0.6 + 0.4 * math.sin(phi * 10)
                    return clamp(base * swirl, 0.0, 1.0)

            # Gravitational deflection (simple Newtonian acceleration)
            acc = [-self.mass * pos[i] / (r ** 3) for i in range(3)]
            dir_vec = _normalize([dir_vec[i] + acc[i] * self.step_size for i in range(3)])
            pos = [pos[i] + dir_vec[i] * self.step_size for i in range(3)]

        return 0.0
