"""Entry point for the ASCII black hole GUI."""

import tkinter as tk
from typing import Optional

from ascii_renderer import ASCIIRenderer
from blackhole_physics import BlackHoleSimulator
import config


def main() -> None:
    root = tk.Tk()
    root.title("ASCII Interstellar Black Hole")

    width, height = config.get_window_size()
    if config.USE_FULLSCREEN:
        root.attributes("-fullscreen", True)
    else:
        root.geometry(f"{width}x{height}")
    canvas = tk.Text(root, width=width, height=height, bg="black")
    canvas.configure(font=("Courier", 10))
    canvas.pack()

    renderer = ASCIIRenderer()
    physics = BlackHoleSimulator(width, height)

    def update_frame() -> Optional[str]:
        brightness = physics.compute_frame()
        frame, colors = renderer.render_colored(brightness)
        canvas.config(state=tk.NORMAL)
        canvas.delete("1.0", tk.END)
        for y, line in enumerate(frame.splitlines()):
            for x, ch in enumerate(line):
                color = colors[y][x]
                tag = color
                if not tag in canvas.tag_names():
                    canvas.tag_config(tag, foreground=color)
                canvas.insert(tk.END, ch, tag)
            canvas.insert(tk.END, "\n")
        canvas.config(state=tk.DISABLED)
        root.after(int(1000 / config.FPS), update_frame)

    update_frame()
    root.mainloop()


if __name__ == "__main__":
    main()
