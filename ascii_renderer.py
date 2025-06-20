"""ASCII rendering module.

This module converts numeric frame data into ASCII strings
for display in the GUI window.
"""

from typing import List

class ASCIIRenderer:
    """Converts brightness matrices to ASCII frames."""

    def __init__(self, charset: str = " .:-=+*#%@"):
        self.charset = charset
        self.levels = len(charset) - 1

    def render(self, brightness: List[List[float]]) -> str:
        """Return a single string representing the ASCII frame."""
        rows = []
        for row in brightness:
            chars = [self._map_value(val) for val in row]
            rows.append("".join(chars))
        return "\n".join(rows)

    def _map_value(self, value: float) -> str:
        """Map a brightness value 0..1 to a character."""
        index = int(max(0.0, min(1.0, value)) * self.levels)
        return self.charset[index]
