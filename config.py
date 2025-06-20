"""Configuration constants for the application.

This module exposes tunable parameters for the GUI, the ASCII renderer and the
placeholder physics model.  Values here are kept simple so that other modules
can easily read them without additional dependencies.
"""

from typing import Tuple


# ---------------------------------------------------------------------------
# Window configuration
# ---------------------------------------------------------------------------

# Whether the application should start in full screen mode.  When set to
# ``True`` the ``FULLSCREEN_WIDTH`` and ``FULLSCREEN_HEIGHT`` values are used to
# size the tkinter window; otherwise ``WINDOWED_WIDTH`` and ``WINDOWED_HEIGHT``
# are used.  The main loop is expected to read these values and configure the
# window accordingly.
USE_FULLSCREEN: bool = False

# Resolution for windowed mode.  The size is intentionally small so the program
# can open as a "widget" on the desktop.
WINDOWED_WIDTH: int = 640
WINDOWED_HEIGHT: int = 360

# Resolution for full screen mode (1920x1080 as requested).
FULLSCREEN_WIDTH: int = 1920
FULLSCREEN_HEIGHT: int = 1080


def get_window_size() -> Tuple[int, int]:
    """Return the width and height that should be used for the window."""

    if USE_FULLSCREEN:
        return FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT
    return WINDOWED_WIDTH, WINDOWED_HEIGHT


# Target frame rate.  The rest of the program may run slower depending on the
# host machine, but the GUI loop will attempt to update at this frequency.
FPS: int = 144


# ---------------------------------------------------------------------------
# ASCII rendering options
# ---------------------------------------------------------------------------

# Character set used to render brightness levels.  The sequence below provides
# a long gradient so the resulting image has more "texture".
CHARSET: str = (
    " .'`^\",:;Il!i><~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
)

# Colour palette for the renderer.  Tkinter accepts hex colour codes; these
# values give a combination of violet and orange/yellow shades.
COLOR_PALETTE = ["#9b5de5", "#f15bb5", "#fee440", "#f8a100"]


# ---------------------------------------------------------------------------
# Placeholder physics parameters based loosely on the "Interstellar" black hole
# ---------------------------------------------------------------------------

# Mass of the black hole in solar masses (Gargantua is roughly 100 million).
MASS: float = 1.0e8

# Dimensionless spin parameter.  In "Interstellar" the black hole was depicted
# with near maximal spin.
SPIN: float = 0.99

# Camera orientation.  ``CAMERA_PITCH`` tilts the view slightly so that the
# accretion disk is not a perfect line, giving a sense of depth.
CAMERA_PITCH: float = -0.2  # radians; negative to look slightly downward
