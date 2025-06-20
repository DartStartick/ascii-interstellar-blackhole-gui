"""Entry point for the ASCII black hole GUI."""

import importlib
import tkinter as tk
from typing import Optional

from ascii_renderer import ASCIIRenderer
from blackhole_physics import BlackHoleSimulator
import config


def main() -> None:
    root = tk.Tk()
    root.title("ASCII Interstellar Black Hole")

    width, height = config.get_window_size()

    canvas = tk.Text(root, width=width, height=height, bg="black")
    canvas.configure(font=("Courier", 10))
    canvas.pack()

    renderer = ASCIIRenderer()
    palette_names = list(renderer.palettes.keys())
    palette_index = 0

    physics = BlackHoleSimulator(width, height)

    def apply_window_size() -> None:
        nonlocal width, height, physics
        width, height = config.get_window_size()
        if config.USE_FULLSCREEN:
            root.attributes("-fullscreen", True)
        else:
            root.attributes("-fullscreen", False)
            root.geometry(f"{width}x{height}")
        canvas.config(width=width, height=height)
        physics = BlackHoleSimulator(width, height)

    apply_window_size()

    def toggle_fullscreen(event: Optional[tk.Event] = None) -> None:
        config.USE_FULLSCREEN = not config.USE_FULLSCREEN
        apply_window_size()

    def toggle_mode(event: Optional[tk.Event] = None) -> None:
        renderer.mode = "mono" if renderer.mode == "color" else "color"

    def cycle_palette(event: Optional[tk.Event] = None) -> None:
        nonlocal palette_index
        palette_index = (palette_index + 1) % len(palette_names)
        renderer.set_palette(palette_names[palette_index])

    def reload_settings(event: Optional[tk.Event] = None) -> None:
        nonlocal renderer, palette_names, palette_index
        importlib.reload(config)
        renderer = ASCIIRenderer()
        palette_names = list(renderer.palettes.keys())
        palette_index = 0
        apply_window_size()

    root.bind("f", toggle_fullscreen)
    root.bind("m", toggle_mode)
    root.bind("p", cycle_palette)
    root.bind("r", reload_settings)
    root.bind("<Escape>", lambda e: root.destroy())

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
