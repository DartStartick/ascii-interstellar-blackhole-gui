"""Entry point for the ASCII black hole GUI."""

import tkinter as tk
from typing import Optional

from ascii_renderer import ASCIIRenderer
from blackhole_physics import BlackHoleSimulator
import config


def main() -> None:
    root = tk.Tk()
    root.title("ASCII Interstellar Black Hole")

    canvas = tk.Text(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)
    canvas.pack()

    renderer = ASCIIRenderer()
    physics = BlackHoleSimulator(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    def update_frame() -> Optional[str]:
        brightness = physics.compute_frame()
        frame = renderer.render(brightness)
        canvas.delete("1.0", tk.END)
        canvas.insert(tk.END, frame)
        root.after(int(1000 / config.FPS), update_frame)

    update_frame()
    root.mainloop()


if __name__ == "__main__":
    main()
