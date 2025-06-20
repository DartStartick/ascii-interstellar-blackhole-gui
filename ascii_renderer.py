"""ASCII rendering module.

This module converts numeric frame data into ASCII strings
for display in the GUI window.
"""

from typing import List, Tuple
import config

class ASCIIRenderer:
    """Converts brightness matrices to ASCII frames and colour information."""

    def __init__(self, charset: str = None, colors: List[str] = None):
        # Use values from the config module if none are provided.
        self.charset = charset if charset is not None else config.CHARSET
        self.colors = colors if colors is not None else config.COLOR_PALETTE
        self.levels = len(self.charset) - 1

    def render(self, brightness: List[List[float]]) -> str:
        """Return a single ASCII string representing the frame."""
        rows = []
        for row in brightness:
            chars = [self._map_value(val) for val in row]
            rows.append("".join(chars))
        return "\n".join(rows)

    def render_colored(self, brightness: List[List[float]]) -> Tuple[str, List[List[str]]]:
        """Return the frame string along with a colour matrix."""
        rows = []
        color_rows: List[List[str]] = []
        for row in brightness:
            chars = []
            colors = []
            for val in row:
                chars.append(self._map_value(val))
                colors.append(self._map_color(val))
            rows.append("".join(chars))
            color_rows.append(colors)
        return "\n".join(rows), color_rows

    def _map_value(self, value: float) -> str:
        """Map a brightness value 0..1 to a character."""
        index = int(max(0.0, min(1.0, value)) * self.levels)
        return self.charset[index]

    def _map_color(self, value: float) -> str:
        """Map a brightness value 0..1 to a colour hex code."""
        index = int(max(0.0, min(1.0, value)) * (len(self.colors) - 1))
        return self.colors[index]
