import tkinter as tk
from constants import (
    COLOR_CARD, COLOR_BORDER, COLOR_TEXT, COLOR_DISABLED,
    COLOR_ACCENT, FONT_BUTTON
)

class Card(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", COLOR_CARD)
        highlightbackground = kwargs.pop("highlightbackground", COLOR_BORDER)
        highlightthickness = kwargs.pop("highlightthickness", 1)
        super().__init__(
            parent,
            bg=bg,
            highlightbackground=highlightbackground,
            highlightthickness=highlightthickness,
            padx=20,
            pady=20,
            **kwargs
        )

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", color="#4a9eff", command=None, width=160, height=45, corner_radius=10):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.current_color = color
        self.text_val = text
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.is_enabled = True

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self.draw()

    def draw(self):
        self.delete("all")
        w, h = self.width, self.height
        r = self.corner_radius
        fill = self.current_color if self.is_enabled else COLOR_DISABLED

        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=fill, outline=fill)
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=fill, outline=fill)
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=fill, outline=fill)
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=fill, outline=fill)
        self.create_rectangle((r, 0, w-r, h), fill=fill, outline=fill)
        self.create_rectangle((0, r, w, h-r), fill=fill, outline=fill)

        self.create_text(w / 2, h / 2, text=self.text_val, fill=COLOR_TEXT, font=FONT_BUTTON)

    def set_enabled(self, enabled):
        self.is_enabled = enabled
        self.draw()

    def _on_enter(self, event):
        if self.is_enabled:
            self.config(cursor="hand2")

    def _on_leave(self, event):
        if self.is_enabled:
            self.config(cursor="")

    def _on_click(self, event):
        if self.is_enabled and self.command:
            self.command()

class ColorSwatchButton(tk.Canvas):
    def __init__(self, parent, command=None, width=110, height=55, corner_radius=10, position_num=1):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.color_name = ""
        self.hex_code = COLOR_DISABLED
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.position_num = position_num
        self.is_enabled = True

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self.draw()

    def set_color_swatch(self, color_name, hex_code):
        self.color_name = color_name
        self.hex_code = hex_code
        self.draw()

    def draw(self):
        self.delete("all")
        w, h = self.width, self.height
        r = self.corner_radius

        fill = self.hex_code if self.is_enabled else COLOR_DISABLED

        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=fill, outline=fill)
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=fill, outline=fill)
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=fill, outline=fill)
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=fill, outline=fill)
        self.create_rectangle((r, 0, w-r, h), fill=fill, outline=fill)
        self.create_rectangle((0, r, w, h-r), fill=fill, outline=fill)

        num_color = "#ffffff" if self.is_enabled else "#888888"
        self.create_text(14, 14, text=str(self.position_num), fill=num_color, font=("Segoe UI", 11, "bold"))

    def set_enabled(self, enabled):
        self.is_enabled = enabled
        self.draw()

    def _on_enter(self, event):
        if self.is_enabled:
            self.config(cursor="hand2")

    def _on_leave(self, event):
        if self.is_enabled:
            self.config(cursor="")

    def _on_click(self, event):
        if self.is_enabled and self.command:
            self.command(self.color_name)