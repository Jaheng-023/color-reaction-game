import random
import tkinter as tk
from tkinter import ttk, messagebox

from constants import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT, GAME_COLORS, KEY_MAPPINGS,
    FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_WORD, FONT_TIP, FUNNY_TIP,
    TOTAL_TRIALS, SIMPLE_TRIALS, MIN_DELAY_MS, MAX_DELAY_MS, TIMEOUT_MS,
    FEEDBACK_DURATION_MS, AGE_GROUPS
)
from widgets import Card, RoundedButton, ColorSwatchButton
from game_logic import GameLogic
from sound import play_sound
from data_manager import save_data

class ColorReactionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

        self.game_logic = None
        self.swatch_buttons = []
        self.position_to_color = {}
        self.timeout_timer = None
        self.delay_timer = None
        self.buttons_enabled = False
        self.transition_shown = False
        self.age_group = ""
        self.experience = ""

        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)

        self.bind("<Key>", self.handle_keypress)
        self.show_start_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=20, padx=50)

        title = tk.Label(card, text="Color Reaction Task", font=FONT_TITLE, fg=COLOR_TEXT, bg=COLOR_CARD)
        title.pack(pady=(0, 10))

        instructions = (
            "Welcome! This activity measures your reaction time.\n\n"
            "• Trials 1-10 (Simple): Match the solid color block shown in the center.\n"
            "• Trials 11-20 (Stroop): Click the button matching the INK COLOR\n"
            "  of the displayed word, ignoring the word text.\n\n"
            "Option buttons are randomized every trial. Use clicks or keys 1 to 6."
        )
        info_label = tk.Label(card, text=instructions, font=FONT_BODY, fg=COLOR_MUTED, bg=COLOR_CARD, justify="left")
        info_label.pack(pady=5)

        tip_label = tk.Label(card, text=FUNNY_TIP, font=FONT_TIP, fg=COLOR_ACCENT, bg=COLOR_CARD)
        tip_label.pack(pady=5)

        input_frame = tk.Frame(card, bg=COLOR_CARD)
        input_frame.pack(pady=10)

        # Participant ID
        pid_label = tk.Label(input_frame, text="Participant ID:", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        pid_label.grid(row=0, column=0, sticky="e", padx=5, pady=4)

        self.pid_entry = tk.Entry(input_frame, font=FONT_BODY, width=12)
        self.pid_entry.grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.pid_entry.focus()

        # Age Group Dropdown
        age_label = tk.Label(input_frame, text="Age Group:", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        age_label.grid(row=1, column=0, sticky="e", padx=5, pady=4)

        self.age_combo = ttk.Combobox(input_frame, values=AGE_GROUPS, state="readonly", font=FONT_BODY, width=10)
        self.age_combo.grid(row=1, column=1, sticky="w", padx=5, pady=4)
        self.age_combo.current(0)

        # Experience Question
        exp_label = tk.Label(input_frame, text="Have you played before?", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        exp_label.grid(row=2, column=0, sticky="e", padx=5, pady=4)

        exp_radio_frame = tk.Frame(input_frame, bg=COLOR_CARD)
        exp_radio_frame.grid(row=2, column=1, sticky="w", padx=5, pady=4)

        self.exp_var = tk.StringVar(value="")
        rb_yes = tk.Radiobutton(
            exp_radio_frame, text="Yes", value="Yes", variable=self.exp_var,
            bg=COLOR_CARD, fg=COLOR_TEXT, selectcolor=COLOR_CARD,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT, font=FONT_BODY
        )
        rb_yes.pack(side="left", padx=5)

        rb_no = tk.Radiobutton(
            exp_radio_frame, text="No", value="No", variable=self.exp_var,
            bg=COLOR_CARD, fg=COLOR_TEXT, selectcolor=COLOR_CARD,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT, font=FONT_BODY
        )
        rb_no.pack(side="left", padx=5)

        self.error_label = tk.Label(card, text="", font=FONT_BODY, fg="#e74c3c", bg=COLOR_CARD)
        self.error_label.pack(pady=4)

        start_btn = RoundedButton(card, text="Start Task", color=COLOR_ACCENT, command=self.validate_and_start, width=160, height=45)
        start_btn.pack(pady=5)

    def validate_and_start(self):
        pid = self.pid_entry.get().strip()
        age = self.age_combo.get()
        exp = self.exp_var.get()

        if not pid or not pid.isalnum():
            self.error_label.config(text="Please enter a valid alphanumeric ID (e.g., P01)")
            return
        if exp not in ["Yes", "No"]:
            self.error_label.config(text="Please select whether you have played before (Yes / No)")
            return

        self.age_group = age
        self.experience = exp
        self.game_logic = GameLogic(pid)
        self.transition_shown = False
        self.show_game_screen()
        self.run_next_trial()

    def show_game_screen(self):
        self.clear_container()

        top_frame = tk.Frame(self.container, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=30, pady=15)

        self.pid_display = tk.Label(top_frame, text=f"ID: {self.game_logic.participant_id}", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_BG)
        self.pid_display.pack(side="left")

        self.trial_label = tk.Label(top_frame, text="Trial 0/20", font=FONT_HEADING, fg=COLOR_TEXT, bg=COLOR_BG)
        self.trial_label.pack(side="left", expand=True)

        self.condition_label = tk.Label(top_frame, text="Condition: -", font=FONT_BODY, fg=COLOR_ACCENT, bg=COLOR_BG)
        self.condition_label.pack(side="right")

        self.progress = ttk.Progressbar(self.container, length=790, mode="determinate")
        self.progress.pack(pady=5)

        self.card = Card(self.container)
        self.card.pack(fill="both", expand=True, padx=30, pady=10)

        self.center_frame = tk.Frame(self.card, bg=COLOR_CARD)
        self.center_frame.pack(expand=True)

        self.swatch_box = tk.Canvas(self.center_frame, width=180, height=100, bg=COLOR_CARD, highlightthickness=0)
        self.swatch_box.pack(pady=5)

        self.stimulus_label = tk.Label(self.center_frame, text="", font=FONT_WORD, bg=COLOR_CARD)
        self.stimulus_label.pack(pady=5)

        self.feedback_label = tk.Label(self.card, text="", font=FONT_HEADING, bg=COLOR_CARD)
        self.feedback_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self.container, bg=COLOR_BG)
        self.buttons_frame.pack(pady=(10, 25))

        self.swatch_buttons = []
        for i in range(1, 7):
            btn = ColorSwatchButton(
                self.buttons_frame,
                command=self.handle_color_click,
                width=110, height=55, position_num=i
            )
            grid_row = 0 if i <= 3 else 1
            grid_col = (i - 1) % 3
            btn.grid(row=grid_row, column=grid_col, padx=12, pady=8)
            self.swatch_buttons.append(btn)

    def show_transition_screen(self):
        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=40, padx=50)

        title = tk.Label(card, text="Part 1 Complete!", font=FONT_TITLE, fg="#2ecc71", bg=COLOR_CARD)
        title.pack(pady=(0, 15))

        info_text = (
            "Great job! You finished the Simple Condition.\n\n"
            "Part 2 (Stroop Condition) is about to begin.\n\n"
            "• Color words will now appear in the center.\n"
            "• Click the button matching the INK COLOR of the word.\n"
            "• Ignore what the word actually says!"
        )
        info_label = tk.Label(card, text=info_text, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD, justify="center")
        info_label.pack(pady=10)

        tip_label = tk.Label(card, text=FUNNY_TIP, font=FONT_TIP, fg=COLOR_ACCENT, bg=COLOR_CARD)
        tip_label.pack(pady=15)

        ready_btn = RoundedButton(
            card,
            text="I'm Ready for Part 2",
            color=COLOR_ACCENT,
            command=self.start_part_2,
            width=200, height=45
        )
        ready_btn.pack(pady=10)

    def start_part_2(self):
        self.transition_shown = True
        self.show_game_screen()
        self.run_next_trial()

    def shuffle_and_update_buttons(self):
        colors = list(GAME_COLORS.items())
        random.shuffle(colors)
        self.position_to_color = {}

        for idx, (name, hex_code) in enumerate(colors):
            self.swatch_buttons[idx].set_color_swatch(name, hex_code)
            self.position_to_color[idx + 1] = name

    def animate_slide_in(self, y_offset=20, step=0):
        if step <= 5:
            offset = int(y_offset * (1 - step / 5))
            self.buttons_frame.pack_configure(pady=(10 + offset, 25))
            self.after(20, lambda: self.animate_slide_in(y_offset, step + 1))

    def reset_center_display(self):
        self.swatch_box.config(bg=COLOR_CARD)
        self.swatch_box.delete("all")
        self.stimulus_label.config(text="")

    def run_next_trial(self):
        self.set_buttons_enabled(False)
        self.reset_center_display()
        self.feedback_label.config(text="")

        if self.game_logic.is_finished():
            self.end_game()
            return

        if self.game_logic.current_trial == SIMPLE_TRIALS and not self.transition_shown:
            self.show_transition_screen()
            return

        trial_info = self.game_logic.next_trial()
        self.trial_label.config(text=f"Trial {trial_info['trial_number']}/{TOTAL_TRIALS}")
        self.condition_label.config(text=f"Condition: {trial_info['condition']}")
        self.progress["value"] = ((trial_info['trial_number'] - 1) / TOTAL_TRIALS) * 100

        self.shuffle_and_update_buttons()
        self.animate_slide_in()

        delay = random.randint(MIN_DELAY_MS, MAX_DELAY_MS)
        self.delay_timer = self.after(delay, self.reveal_stimulus)

    def reveal_stimulus(self):
        self.game_logic.start_stimulus()
        self.set_buttons_enabled(True)
        condition = self.game_logic.get_condition()

        ink_hex = GAME_COLORS[self.game_logic.target_color]

        if condition == "Simple":
            self.swatch_box.config(bg=ink_hex)
            self.stimulus_label.config(text="")
        else:
            self.swatch_box.config(bg=COLOR_CARD)
            word = self.game_logic.target_word.upper()
            self.stimulus_label.config(text=word, fg=ink_hex)

        self.timeout_timer = self.after(TIMEOUT_MS, self.handle_timeout)

    def set_buttons_enabled(self, enabled):
        self.buttons_enabled = enabled
        for btn in self.swatch_buttons:
            btn.set_enabled(enabled)

    def handle_color_click(self, selected_color):
        if not self.buttons_enabled:
            return
        if self.timeout_timer:
            self.after_cancel(self.timeout_timer)
            self.timeout_timer = None

        self.set_buttons_enabled(False)
        self.reset_center_display()

        record = self.game_logic.process_response(selected_color)
        record["age_group"] = self.age_group
        record["experience"] = self.experience
        play_sound(record["correct"])

        if record["correct"]:
            self.feedback_label.config(text=f"CORRECT! {record['reaction_time_ms']} ms", fg="#2ecc71")
        else:
            self.feedback_label.config(text=f"WRONG! {record['reaction_time_ms']} ms", fg="#e74c3c")

        self.after(FEEDBACK_DURATION_MS, self.run_next_trial)

    def handle_timeout(self):
        self.set_buttons_enabled(False)
        self.reset_center_display()

        record = self.game_logic.process_response(None)
        record["age_group"] = self.age_group
        record["experience"] = self.experience
        play_sound(False)

        self.feedback_label.config(text="TIMEOUT!", fg="#e74c3c")
        self.after(FEEDBACK_DURATION_MS, self.run_next_trial)

    def handle_keypress(self, event):
        if self.buttons_enabled and event.char in ["1", "2", "3", "4", "5", "6"]:
            pos_num = int(event.char)
            color_name = self.position_to_color.get(pos_num)
            if color_name:
                self.handle_color_click(color_name)

    def end_game(self):
        try:
            save_data(self.game_logic.trial_records, self.age_group, self.experience)
            saved_msg = "Data saved successfully to CSV."
        except Exception as e:
            saved_msg = f"Failed to save data: {e}"
            messagebox.showerror("Error", saved_msg)

        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=50, padx=50)

        thank_label = tk.Label(card, text="Thank You!", font=FONT_TITLE, fg=COLOR_TEXT, bg=COLOR_CARD)
        thank_label.pack(pady=15)

        msg_label = tk.Label(card, text=f"Experiment Complete.\n{saved_msg}", font=FONT_BODY, fg=COLOR_MUTED, bg=COLOR_CARD)
        msg_label.pack(pady=10)

        restart_btn = RoundedButton(card, text="Main Menu", color=COLOR_ACCENT, command=self.show_start_screen, width=160, height=45)
        restart_btn.pack(pady=20)   