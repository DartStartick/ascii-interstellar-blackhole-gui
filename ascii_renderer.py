"""ASCII rendering module.

This module converts numeric frame data into ASCII strings
for display in the GUI window.
"""

from typing import Dict, List, Tuple, Union

import config

# Built-in palettes that can be selected by name.  Additional palettes
# can be registered at runtime via :func:`register_palette`.
DEFAULT_PALETTES: Dict[str, List[str]] = {
    "violet_orange": config.COLOR_PALETTE,
    "grayscale": ["#000000", "#555555", "#aaaaaa", "#ffffff"],
}

class ASCIIRenderer:
    """Converts brightness matrices to ASCII frames and colour information."""

    def __init__(
        self,
        charset: str | None = None,
        palette: Union[str, List[str], None] = None,
        mode: str = "color",
    ) -> None:
        """Initialise the renderer.

        Parameters
        ----------
        charset:
            Sequence of characters ordered from dark to light.
        palette:
            Either a list of colour codes or the name of a built-in palette.
        mode:
            ``"color"`` or ``"mono"``. In monochrome mode ``_map_color``
            returns the same colour for all brightness values.
        """

        self.charset = charset if charset is not None else config.CHARSET
        self.mode = mode
        self.palettes: Dict[str, List[str]] = DEFAULT_PALETTES.copy()
        self.set_palette(palette if palette is not None else "violet_orange")

        self.levels = len(self.charset) - 1

    # ------------------------------------------------------------------
    # Palette management
    # ------------------------------------------------------------------

    def set_palette(self, palette: Union[str, List[str]]) -> None:
        """Select a palette by name or list of colours."""
        if isinstance(palette, str):
            self.colors = self.palettes.get(palette, config.COLOR_PALETTE)
        else:
            self.colors = list(palette)
        self.color_levels = max(1, len(self.colors) - 1)

    def register_palette(self, name: str, colors: List[str]) -> None:
        """Register a new palette that can be used with ``set_palette``."""
        self.palettes[name] = colors

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
        if self.mode == "mono":
            return self.colors[0]

        index = int(max(0.0, min(1.0, value)) * self.color_levels)
        return self.colors[index]
