import tkinter as tk
from constants import (
    COLOR_CARD, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED,
    COLOR_DISABLED, COLOR_PRIMARY, COLOR_ACCENT, COLOR_PINK, FONT_BUTTON
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
            padx=25,
            pady=25,
            **kwargs
        )

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", color=COLOR_PRIMARY, hover_color=COLOR_ACCENT, command=None, width=180, height=45, corner_radius=10):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.base_color = color
        self.hover_color = hover_color
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

        text_color = "#FFFFFF" if self.is_enabled else "#888888"
        self.create_text(w / 2, h / 2, text=self.text_val, fill=text_color, font=FONT_BUTTON)

    def set_enabled(self, enabled):
        self.is_enabled = enabled
        self.draw()

    def _on_enter(self, event):
        if self.is_enabled:
            self.current_color = self.hover_color
            self.config(cursor="hand2")
            self.draw()

    def _on_leave(self, event):
        if self.is_enabled:
            self.current_color = self.base_color
            self.config(cursor="")
            self.draw()

    def _on_click(self, event):
        if self.is_enabled and self.command:
            self.command()

class ColorSwatchButton(tk.Canvas):
    def __init__(self, parent, command=None, width=105, height=52, corner_radius=10, position_num=1):
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

        num_color = "#FFFFFF" if self.is_enabled else "#888888"
        self.create_text(14, 14, text=str(self.position_num), fill=num_color, font=("Segoe UI", 10, "bold"))

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

class TrialHistoryStack(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLOR_CARD,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=12,
            pady=10,
            **kwargs
        )
        self.title_label = tk.Label(
            self,
            text="Recent Trials (Last 5)",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD
        )
        self.title_label.pack(anchor="w", pady=(0, 4))

        self.history_frame = tk.Frame(self, bg=COLOR_CARD)
        self.history_frame.pack(fill="x", expand=True)
        self.records = []
        self.update_display()

    def add_record(self, trial_num, condition, rt_ms, correct):
        self.records.insert(0, {
            "trial": trial_num,
            "condition": condition,
            "rt": rt_ms,
            "correct": correct
        })
        if len(self.records) > 5:
            self.records.pop()
        self.update_display()

    def clear(self):
        self.records = []
        self.update_display()

    def update_display(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not self.records:
            empty_lbl = tk.Label(
                self.history_frame,
                text="No trials yet",
                font=("Segoe UI", 9, "italic"),
                fg=COLOR_MUTED,
                bg=COLOR_CARD
            )
            empty_lbl.pack(anchor="w", pady=4)
            return

        for rec in self.records:
            status_icon = "✓" if rec["correct"] else "✗"
            status_color = "#2ECC71" if rec["correct"] else "#E74C3C"
            rt_text = "TIMEOUT" if (rec["rt"] >= 2000.0 and not rec["correct"]) else f"{rec['rt']} ms"

            row = tk.Frame(self.history_frame, bg=COLOR_CARD)
            row.pack(fill="x", pady=2)

            t_lbl = tk.Label(
                row, text=f"T{rec['trial']} ({rec['condition'][:1]}):",
                font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_CARD,
                width=7, anchor="w"
            )
            t_lbl.pack(side="left")

            rt_lbl = tk.Label(
                row, text=rt_text,
                font=("Segoe UI", 9), fg=COLOR_MUTED, bg=COLOR_CARD,
                width=9, anchor="w"
            )
            rt_lbl.pack(side="left")

            st_lbl = tk.Label(
                row, text=status_icon,
                font=("Segoe UI", 9, "bold"), fg=status_color, bg=COLOR_CARD
            )
            st_lbl.pack(side="right")